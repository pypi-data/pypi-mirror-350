"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.


        Example:

        ```yaml
        Lowes:
          type: reviews
          use_proxies: true
          paid_proxy: true
          api_token: xxx
        ```

    """
import asyncio
from collections.abc import Callable
import random
import httpx
import pandas as pd
import backoff
# Internals
from ..exceptions import (
    ComponentError,
    ConfigError,
    NotSupported
)
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, bad_gateway_exception


class Lowes(ReviewScrapper):
    """Lowes.

    Combining API Key and Web Scrapping, this component will be able to extract
    Lowes Information (reviews, etc).
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super(Lowes, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        self.cookies = {
            "dbidv2": "956aa8ea-87f3-4068-96a8-3e2bdf4e84ec",
            "al_sess": "FuA4EWsuT07UWryyq/3foLUcOGRVVGi7yYKO2imCjWnuWxkaJXwqJRDEw8CjJaWJ",
            # Add other necessary cookies here
            # Ensure tokens are valid and not expired
        }
        self.headers: dict = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "www.lowes.com",
            "Pragma": "no-cache",
            "Origin": "https://www.lowes.com",
            "Referer": "https://www.lowes.com/pd/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": random.choice(ua)
        }
        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(Lowes, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('TARGET_API_KEY')  # noqa
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"BestBuy: Unable to found Function {self._fn} in Target Component."
            )

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_reviews(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['sku']
            page_size = 10  # fixed size
            current_offset = 0
            max_pages = 20  # Maximum number of pages to fetch
            all_reviews = []
            total_reviews = 0
            try:
                while current_offset < max_pages * page_size:
                    if current_offset == 0:
                        payload = {
                            "sortBy": "newestFirst"
                        }
                    else:
                        payload = {
                            "sortBy": "newestFirst",
                            "offset": current_offset
                        }
                    url = f"https://www.lowes.com/rnr/r/get-by-product/{sku}"
                    result = await self.api_get(
                        url=url,
                        cookies=cookies,
                        params=payload,
                        headers=self.headers
                    )
                    if not result:
                        self._logger.warning(
                            f"No Product Reviews found for {sku}."
                        )
                        break
                    # Extract the reviews data from the API response
                    reviews_section = result.get('results', [])
                    total_reviews = result.get('totalResults', 0)
                    if not reviews_section:
                        self._logger.info(f"No more reviews found for SKU {sku} at offset {current_offset}.")
                        break
                    if len(reviews_section) == 0:
                        break
                    all_reviews.extend(reviews_section)
                    # Update total_reviews

                    # Check if we've fetched all reviews
                    if len(all_reviews) >= total_reviews:
                        self._logger.info(f"Fetched all reviews for SKU {sku}.")
                        break
                    current_offset += page_size  # Move to the next page
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
                # Extract relevant fields
                # Combine with original row data
                review_data = row.to_dict()
                review = {
                    **review_data,
                    "id": item.get("id"),
                    "legacyId": item.get("legacyId"),
                    "title": item.get("title"),
                    "review": item.get("reviewText"),
                    "rating": item.get("rating"),
                    "isRecommended": item.get("isRecommended"),
                    "userNickname": item.get("userNickname"),
                    "submissionTime": item.get("submissionTime"),
                    "verifiedPurchaser": item.get("verifiedPurchaser"),
                    "helpfulVoteCount": item.get("helpfulVoteCount"),
                    "notHelpfulVoteCount": item.get("notHelpfulVoteCount"),
                    "clientResponses": item.get("clientResponses"),
                    "relevancyScore": item.get("relevancyScore"),
                    "productId": item.get("productId"),
                }
                review['total_reviews'] = total_reviews
                # Optionally, handle client responses
                if review["clientResponses"]:
                    # For simplicity, concatenate all responses into a single string
                    responses = []
                    for response in review["clientResponses"]:
                        response_text = response.get("response", "")
                        responses.append(response_text.strip())
                    review["clientResponses"] = " | ".join(responses)
                reviews.append(review)
            self._logger.info(
                f"Fetched {len(reviews)} reviews for SKU {sku}."
            )
            return reviews

    async def reviews(self):
        """reviews.

        Target Product Reviews.
        """
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.lowes.com',
                path='/'
            )

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

        # at the end, adding a column for origin of reviews:
        reviews_df['origin'] = 'lowes'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Reviews: {len(reviews_df)}"
        )

        # Override previous dataframe:
        self.data = reviews_df

        # return existing data
        return self.data

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _product_details(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            sku = row['sku']
            storeid = row['store_id']
            zipcode = row['zipcode'],
            state_code = row['state_code']
            payload = {
                "nearByStore": storeid,
                "zipState": state_code,
                "quantity": 1
            }
            try:
                # url = "https://www.lowes.com/lowes-proxy/wpd/1000379005/productdetail/1845/Guest/60639?nearByStore=1845&zipState=IL&quantity=1"
                # url = f"https://www.lowes.com/wpd/{sku}/productdetail/{storeid}/Guest/{zipcode}"
                url = f"https://www.lowes.com/lowes-proxy/wpd/{sku}/productdetail/{storeid}/Guest/{zipcode}"
                result = await self.api_get(
                    url=url,
                    # cookies=cookies,
                    # params=payload,
                    headers=self.headers
                )
                if not result:
                    self._logger.warning(
                        f"No Product Details found for {sku}."
                    )
                    return []
                # Extract the product details data from the API response
                print('RESULT > ', result)
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return []
            except Exception as ex:
                print(ex)
                self._logger.error(f"An error occurred: {ex}")
                return []

    async def product_details(self):
        """product_details.

        Get Product Details from Lowes URL.
        """
        self.cookies = {}
        httpx_cookies = httpx.Cookies()
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.lowes.com',
                path='/'
            )

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._product_details(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]
        # Gather results concurrently
        all_products_nested = await self._processing_tasks(tasks)

        # Flatten the list of lists
        all_products = [product for products in all_products_nested for product in products]

        # Convert to DataFrame
        _df = pd.DataFrame(all_products)

        # at the end, adding a column for origin of reviews:
        _df['origin'] = 'lowes'

        # show the num of rows in final dataframe:
        self._logger.notice(
            f"Ending Product Details: {len(_df)}"
        )

        # Override previous dataframe:
        self.data = _df

        # return existing data
        return self.data
