import asyncio
import aiohttp
from typing import Any, Dict
from collections.abc import Callable
import random
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import httpx
import pandas as pd
import backoff
import ssl
from navconfig.logging import logging
# Internals
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported,
    ConfigError
)
from .flow import FlowComponent
from ..interfaces import HTTPService, SeleniumService
from ..interfaces.http import ua


logging.getLogger(name='selenium.webdriver').setLevel(logging.WARNING)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)
logging.getLogger(name='seleniumwire').setLevel(logging.WARNING)


ProductPayload = {
    "locationId": None,
    "zipCode": None,
    "showOnShelf": True,
    "lookupInStoreQuantity": True,
    "xboxAllAccess": False,
    "consolidated": True,
    "showOnlyOnShelf": False,
    "showInStore": True,
    "pickupTypes": [
        "UPS_ACCESS_POINT",
        "FEDEX_HAL"
    ],
    "onlyBestBuyLocations": True,
    "items": [
        {
            "sku": None,
            "condition": None,
            "quantity": 1,
            "itemSeqNumber": "1",
            "reservationToken": None,
            "selectedServices": [],
            "requiredAccessories": [],
            "isTradeIn": False,
            "isLeased": False
        }
    ]
}


def bad_gateway_exception(exc):
    """Check if the exception is a 502 Bad Gateway error."""
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 502


class BestBuy(FlowComponent, SeleniumService, HTTPService):
    """BestBuy.

    Combining API Key and Web Scrapping, this component will be able to extract
    Best Buy Information (stores, products, Product Availability, etc).


        Example:

        ```yaml
        BestBuy:
          type: availability
          product_info: false
          brand: Bose
        ```

    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._fn = kwargs.pop('type', None)
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        self.product_info: bool = kwargs.get('product_info', False)
        if not self._fn:
            raise ConfigError(
                "BestBuy: require a `type` Function to be called, ex: availability"
            )
        super(BestBuy, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        ctt_list: list = [
            "f3dbf688e45146555bb2b8604a993601",
            "06f4dfe367e87866397ef32302f5042e",
            "4e07e03ff03f5debc4e09ac4db9239ac"
        ]
        sid_list: list = [
            "d4fa1142-2998-4b68-af78-46d821bb3e1f",
            "9627390e-b423-459f-83ee-7964dd05c9a8"
        ]
        self.cookies = {
            # "CTT": ,
            "CTT": random.choice(ctt_list),
            "SID": random.choice(sid_list),
            "bby_rdp": "l",
            "bm_sz": "9F5ED0110AF18594E2347A89BB4AB998~YAAQxm1lX6EqYHGSAQAAw+apmhkhXIeGYEc4KnzUMsjeac3xEoQmTNz5+of62i3RXQL6fUI+0FvCb/jgSjiVQOcfaSF+LdLkOXP1F4urgeIcqp/dBAhu5MvZXaCQsT06bwr7j21ozhFfTTWhjz1HmZN8wecsE6WGbK6wXp/33ODKlLaGWkTutqHbkzvMiiHXBCs9hT8jVny0REfita4AfqTK85Y6/M6Uq4IaDLPBLnTtJ0cTlPHk1HmkG5EsnI46llghcx1KZnCGnvZfHdb2ME9YZJ2GmC2b7dNmAgyL/gSVpoNdCJOj5Jk6z/MCVhZ81OZfX4S01E2F1mBGq4uV5/1oK2KR4YgZP4dsTN8izEEPybUKGY3CyM1gOUc=~3556420~4277810",  # noqa
            "bby_cbc_lb": "p-browse-e",
            "intl_splash": "false"
        }
        self.headers: dict = {
            "Host": "www.bestbuy.com",
            "Referer": "https://www.bestbuy.com/",
            "X-Requested-With": "XMLHttpRequest",
            "TE": "trailers",
            "Accept-Language": "en-US,en;q=0.5",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **self.headers
        }
        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(BestBuy, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        #else:
        #    raise DataNotFound(
        #        "Data Not Found",
        #        status=404
        #    )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('BEST_BUY_API_KEY')
        # if self._fn == 'availability':
            # if not hasattr(self, 'brand'):
            #     raise ConfigError(
            #         "BestBuy: A Brand is required for using Product Availability"
            #     )
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"BestBuy: Unable to found Function {self._fn} in BBY Component."
            )

    def _get_search_url(self, brand: str, sku: str) -> str:
        front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
        middle_url = "&searchType=search&st="
        page_count = 1
        # TODO: Get the Brand and Model from the Component.
        search_term = f'{sku}'
        end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"  # noqa
        url = front_url + str(page_count) + middle_url + search_term + end_url
        print('SEARCH URL: ', url)
        return url

    async def _extract_product_info(self, product_element):
        """Extract product information from a specific product element"""
        try:
            # Get the SKU from data-testid attribute (primary method)
            sku_id = product_element.get("data-testid")
            
            # Fallback: Try to find SKU in the attribute div
            if not sku_id:
                sku_element = product_element.select_one('div.attribute:-soup-contains("SKU") span.value')
                if sku_element:
                    sku_id = sku_element.text.strip()
            
            # Get product title through the product link
            title_element = product_element.select_one('.product-list-item-title a, h4.sku-title a, a.product-list-item-link')
            if not title_element:
                title_element = product_element.select_one('a.product-list-item-link')
            
            if not title_element:
                return None
            
            title = title_element.text.strip()
            
            # Find price
            price_element = product_element.select_one('div[data-testid="medium-customer-price"], div.customer-price.medium, .priceView-customer-price span, .price-block span')
            price = price_element.text.strip() if price_element else "N/A"
            
            # Image
            image_element = product_element.select_one('img.product-image, img')
            image = image_element['src'] if image_element and 'src' in image_element.attrs else None
            
            # URL
            url_element = title_element
            url = "{url}".format(
                url=url_element['href']
            ) if url_element and 'href' in url_element.attrs else None
            
            self._logger.notice(f':: Product URL: {url}')
            
            # Get model
            model_element = product_element.select_one('div.attribute:-soup-contains("Model") span.value')
            model_value = model_element.text.strip() if model_element else self.model
            
            return {
                "sku": sku_id,
                "brand": self.brand,
                "product_name": title,
                "image_url": image,
                "price": price,
                "url": url
            }
        except Exception as e:
            self._logger.error(f"Error extracting product info: {e}")
            return None

    async def _product_info(self, idx, row):
        async with self.semaphore:
            # Extract model, brand and SKU from the row
            model = row['model']
            brand = row['brand']
            sku = row['sku'] if 'sku' in row else None
            
            # Configure these values for searching
            self.brand = brand
            self.sku = sku
            self.model = model
            
            try:
                # Generate the search URL
                url = self._get_search_url(brand, model)
                
                # Initialize Selenium driver if it doesn't exist
                if not self._driver:
                    await self.get_driver()
                
                # Navigate to the URL
                await self.get_page(url)
                
                # Initially assume we won't find the product
                self.data.loc[idx, 'enabled'] = False
                
                # Execute progressive scroll with longer pauses to ensure dynamic content loads
                self._execute_scroll(scroll_pause_time=4.0, max_scrolls=10)
                
                # Add additional wait after scroll to ensure complete load
                await asyncio.sleep(3)  # Additional wait after completing all scrolls
                
                # Get the HTML content of the page after scrolling
                page_content = self._driver.page_source
                
                # Parse the HTML content
                soup = BeautifulSoup(page_content, 'html.parser')
                
                # Find all product items - using the correct class from the HTML analysis
                product_items = soup.find_all('li', {'class': ['product-list-item']})
                if not product_items:
                    # Fallback to other possible class names
                    product_items = soup.find_all('li', {'class': ['sku-item']})
                
                # Debug: Print how many products were found
                print(f"Found {len(product_items)} products in search results")
                print(f"Searching for: Model={self.model}, SKU={self.sku}")
                
                # Process each product item
                for item in product_items:
                    try:
                        # Get the SKU from data-testid
                        sku_id = item.get("data-testid")
                        
                        # Try to get the model
                        model_element = item.select_one('div.attribute:-soup-contains("Model") span.value')
                        model_value = model_element.text.strip() if model_element else None
                        
                        # Debug information
                        if model_value or sku_id:
                            print(f"Found product: SKU={sku_id}, Model={model_value}")
                            if self.model:
                                print(f"Comparing with our Model={self.model}")
                            if self.sku:
                                print(f"Comparing with our SKU={self.sku}")
                        
                        # Check if either SKU or model matches
                        sku_match = self.sku and sku_id == self.sku
                        model_match = False
                        if model_value and self.model:
                            # More flexible comparison
                            model_match = (
                                model_value.strip() == self.model.strip() or
                                model_value.lower() == self.model.lower() or
                                model_value.replace(" ", "") == self.model.replace(" ", "") or
                                self.model in model_value or
                                model_value in self.model
                            )
                        
                        # If we have a match, extract product information
                        if sku_match or model_match:
                            self._logger.info(f"Found matching product - SKU: {sku_id}, Model: {model_value}")
                            
                            # Extract product information from this element
                            product_info = await self._extract_product_info(item)
                            
                            if product_info:
                                # Update the DataFrame with product information
                                for key, value in product_info.items():
                                    if key in self.data.columns:
                                        self.data.loc[idx, key] = value
                                    else:
                                        self.data.at[idx, key] = value
                                
                                # Mark as enabled since we found a match
                                self.data.loc[idx, 'enabled'] = True
                                
                                # We found our product, no need to continue
                                return row
                    except Exception as e:
                        print(f"Error processing product: {e}")
                
                # If we got here, no match was found
                self._logger.warning(f"No matching product found for {brand} {model} / {sku}")
                return row
                
            except Exception as exc:
                self._logger.error(f"Error during product search for {brand} {model}: {exc}")
                return row

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _check_store_availability(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            zipcode = row['zipcode']
            location_code = str(row['location_code'])
            sku = row['sku']
            brand = row['brand']
            payload = ProductPayload.copy()
            payload["locationId"] = location_code
            payload["zipCode"] = zipcode
            for item in payload["items"]:
                item["sku"] = sku

            # checking if this current store is already marked as checked:
            matching_store = self.data[
                (self.data['location_code'] == location_code) & (self.data['sku'] == sku)
            ]
            if not matching_store.empty and matching_store.iloc[0]['checked'] is True:
                # exit without making any HTTP call.
                return row
            try:
                result = await self.api_post(
                    url="https://www.bestbuy.com/productfulfillment/c/api/2.0/storeAvailability",
                    cookies=cookies,
                    payload=payload
                )
                self._num_iterations += 1
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return row
            except Exception as ex:
                self._logger.error(f"An error occurred: {ex}")
                return row

            if not result:
                self._logger.warning(
                    f"No availability data found for {sku} at zipcode {zipcode}"
                )
                return row

            # Extract the availability data from the API response
            items = result.get('ispu', {}).get('items', [])
            for item in items:
                locations = item.get('locations', [])
                for location in locations:
                    self.data.loc[idx, 'enabled'] = False if result.get('consolidatedButtonState', {}).get('buttonState', '') == 'NOT_AVAILABLE' else True
                    lid = location.get('locationId')
                    # Find matching store and SKU in DataFrame
                    matching_store = self.data[
                        (self.data['location_code'] == lid) & (self.data['sku'] == sku)
                    ]
                    if not matching_store.empty:
                        idx = matching_store.index[0]
                        if self.data.loc[idx, 'checked'] is True:
                            print('Already checked, continue ...')
                            continue  # Skip this row if it's already marked as checked
                        if 'availability' not in location:
                            self.data.loc[idx, 'locationId'] = lid
                            self.data.loc[idx, 'checked'] = True
                            continue  # This store doesn't have availability
                        print(f'Found matching store {lid} for sku {sku}')

                        # Update the DataFrame row with new availability data
                        self.data.loc[idx, ['brand', 'location_data']] = [brand, location]
                        for key, val in location.items():
                            if key in self.data.columns:
                                self.data.at[idx, key] = val
                            else:
                                self.data.at[idx, key] = None
                            if key == 'inStoreAvailability':
                                try:
                                    self.data.loc[idx, 'availableInStoreQuantity'] = val.get(
                                        'availableInStoreQuantity', 0
                                    )
                                except KeyError:
                                    self.data.loc[idx, 'availableInStoreQuantity'] = None
                        # Mark the row as checked
                        self.data.loc[idx, 'checked'] = True
            return row

    def column_exists(self, column: str, default_val: Any = None):
        if column not in self.data.columns:
            self._logger.warning(
                f"Column {column} does not exist in the Dataframe"
            )
            self.data[column] = default_val
            return False
        return True

    async def availability(self):
        """availability.

        Best Buy Product Availability.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.bestbuy.com',
                path='/'
            )

        # define the columns returned:
        self.column_exists('brand')
        self.column_exists('location_data')
        self.column_exists('locationId')
        self.column_exists('availability')
        self.column_exists('inStoreAvailability')
        self.column_exists('onShelfDisplay', False)
        self.column_exists('availableInStoreQuantity', 0)
        self.column_exists('enabled', False)

        # With available cookies, iterate over dataframe for stores:
        self.data['checked'] = False  # Add 'checked' flag column

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._check_store_availability(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]

        self._num_iterations = 0
        await self._processing_tasks(tasks)

        self.add_metric('NUM_HTTP_CALLS', self._num_iterations)

        # show the num of rows in final dataframe:
        self._logger.notice(
            "Ending Checking Availability."
        )

        # return existing data
        return self.data

    async def products(self):
        """
            Fetch all products from the Best Buy API by paginating through all pages.

            Returns:
                list: A combined list of all products from all pages.
        """
        all_products = []
        current_page = 1
        total_pages = None
        show = 'sku,upc,modelNumber,name,manufacturer,type,salePrice,url,productTemplate,classId,class,subclassId,subclass,department,image,longDescription,customerReviewCount,customerReviewAverage'
        self._num_iterations = 0
        try:
            while True:
                url = f"https://api.bestbuy.com/v1/products?page={current_page}&pageSize=100&apiKey={self.api_token}&show={show}&format=json"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as result:
                        response = await result.json()
                        #response = await self.api_get(url, httpx_cookies)
                        self._num_iterations += 1

                        # Extract products from the response
                        products = response.get("products", [])
                        if len(products) == 0:
                            continue
                        all_products.extend(products)
                        #all_products += products

                        # Pagination control
                        current_page = response.get("currentPage", current_page)
                        total_pages = response.get("totalPages", current_page) if total_pages is None else total_pages
                        self._logger.debug(f"{url}\n    Current Page: {current_page}, Total Pages: {total_pages}, Products: {len(all_products)}")

                        # Break if we've processed all pages
                        if current_page >= total_pages:  # or current_page == 3:
                            break

                        # Increment page for the next request
                        current_page += 1

            self.add_metric('NUM_HTTP_CALLS', self._num_iterations)
            return pd.DataFrame(all_products)

        except Exception as exc:
            self._logger.error(f"Error while fetching products: {exc}")
            return []

    async def stores(self):
        """
            Fetch all stores from the Best Buy API by paginating through all pages.

            Returns:
                list: A combined list of all stores from all pages.
        """
        all_stores = []
        current_page = 1
        total_pages = None
        self._num_iterations = 0
        try:
            while True:
                url = f"https://api.bestbuy.com/v1/stores?page={current_page}&pageSize=100&apiKey={self.api_token}&format=json"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as result:
                        response = await result.json()
                        self._num_iterations += 1

                        # Extract stores from the response
                        stores = response.get("stores", [])
                        if len(stores) == 0:
                            continue
                        all_stores.extend(stores)
                        # Pagination control
                        current_page = response.get("currentPage", current_page)
                        total_pages = response.get("totalPages", current_page) if total_pages is None else total_pages
                        self._logger.debug(f"{url}\n    Current Page: {current_page}, Total Pages: {total_pages}, Stores: {len(all_stores)}")

                        # Break if we've processed all pages
                        if current_page >= total_pages:
                            break

                        # Increment page for the next request
                        current_page += 1

            self.add_metric('NUM_HTTP_CALLS', self._num_iterations)
            return pd.DataFrame(all_stores)

        except Exception as exc:
            self._logger.error(f"Error while fetching stores: {exc}")
            return []

    @backoff.on_exception(
        backoff.expo,
        (httpx.TimeoutException, httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=3,
        jitter=backoff.full_jitter,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_reviews(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['sku']
            pagesize = 20
            max_pages = 20    # Maximum number of pages to fetch
            current_page = 1
            all_reviews = []
            total_reviews = 0
            try:
                while current_page <= max_pages:
                    payload = {
                        "page": current_page,
                        "pageSize": pagesize,
                        "sort": "MOST_RECENT",
                        # "variant": "A",
                        # "verifiedPurchaseOnly": "true",
                        "sku": sku
                    }
                    result = await self.api_get(
                        url="https://www.bestbuy.com/ugc/v2/reviews",
                        cookies=cookies,
                        params=payload
                    )
                    await asyncio.sleep(0.1)
                    total_reviews = result.get('totalResults', 0)
                    if not result:
                        self._logger.warning(
                            f"No Product Reviews found for {sku}."
                        )
                        break
                    # Extract the reviews data from the API response
                    items = result.get('topics', [])
                    if len(items) == 0:
                        break

                    all_reviews.extend(items)

                    # Determine if we've reached the last page
                    total_pages = result.get('totalPages', max_pages)
                    if current_page >= total_pages:
                        break
                    current_page += 1  # Move to the next page
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                self._logger.error(f"An error occurred: {ex}")
                return []

            # Extract the reviews data from the API response
            reviews = []
            for item in all_reviews:
                # Exclude certain keys
                filtered_item = {k: v for k, v in item.items() if k not in ('brandResponses', 'badges', 'photos', 'secondaryRatings')}
                # Combine with original row data
                review_data = row.to_dict()
                review_data['total_reviews'] = total_reviews
                review_data.update(filtered_item)
                reviews.append(review_data)
            self._logger.info(
                f"Fetched {len(reviews)} reviews for SKU {sku}."
            )
            await asyncio.sleep(random.randint(1, 3))
            return reviews

    async def reviews(self):
        """reviews.

        Best Buy Product Reviews.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.bestbuy.com',
                path='/'
            )

        # With available cookies, iterate over dataframe for stores:
        self.data['checked'] = False  # Add 'checked' flag column

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_reviews(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_reviews_nested = await self._processing_tasks(tasks)

        # Flatten the list of lists
        all_reviews = [review for reviews in all_reviews_nested for review in reviews]

        # Convert to DataFrame
        reviews_df = pd.DataFrame(all_reviews)

        # Remove duplicates based on the review 'id' column
        if 'id' in reviews_df.columns:
            reviews_df = reviews_df.drop_duplicates(subset=['id'])

        # rename the "text" column as "review" and the "id" column as "reviewid"
        reviews_df.rename(columns={'text': 'review', 'id': 'reviewid'}, inplace=True)

        # at the end, adding a column for origin of reviews:
        reviews_df['origin'] = 'bestbuy'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Reviews: {len(reviews_df)}"
        )

        # Override previous dataframe:
        self.data = reviews_df

        # return existing data
        return self.data

    async def product(self):
        """product.

        Best Buy Product Information.
        """
        # Ensure required columns exist in the DataFrame
        self.column_exists('model')
        self.column_exists('brand')
        self.column_exists('sku')
        self.column_exists('product_name')
        self.column_exists('image_url')
        self.column_exists('price')
        self.column_exists('url')
        self.column_exists('enabled', False)
        
        # Set headless to False for debugging
        self.headless = True
        
        # Always set as_mobile to False to ensure desktop mode
        self.as_mobile = False
        
        # Initialize Selenium driver
        if not self._driver:
            await self.get_driver()
        
        # Create tasks to process each row in the DataFrame
        tasks = [
            self._product_info(
                idx,
                row
            ) for idx, row in self.data.iterrows()
        ]
        
        # Process tasks concurrently
        await self._processing_tasks(tasks)

        # Add origin column
        self.data['origin'] = 'bestbuy'

        # Close Selenium driver after completing all tasks
        self.close_driver()
        
        # Return the updated DataFrame
        return self.data

    async def run(self):
        # we need to call the "function" for Best Buy Services.
        fn = getattr(self, self._fn)
        result = None
        if not callable(fn):
            raise ComponentError(
                f"Best Buy: Function {self._fn} doesn't exists."
            )
        try:
            result = await fn()
        except (ComponentError, TimeoutError, NotSupported):
            raise
        except Exception as exc:
            raise ComponentError(
                f"BestBuy: Unknown Error: {exc}"
            ) from exc
        # Print results
        print(result)
        print("::: Printing Column Information === ")
        for column, t in result.dtypes.items():
            print(column, "->", t, "->", result[column].iloc[0])
        self._result = result
        return self._result

    def split_parts(self, task_list, num_parts: int = 5) -> list:
        part_size = len(task_list) // num_parts
        remainder = len(task_list) % num_parts
        parts = []
        start = 0
        for i in range(num_parts):
            # Distribute the remainder across the first `remainder` parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(task_list[start:end])
            start = end
        return parts

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        for chunk in self.split_parts(tasks, self.task_parts):
            result = await asyncio.gather(*chunk, return_exceptions=False)
            results.extend(result)
        return results
