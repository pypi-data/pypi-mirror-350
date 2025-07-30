from collections.abc import Callable
import asyncio
from typing import Any
# Bot Infraestructure:
from parrot.bots.basic import BasicBot
from .flow import FlowComponent
from ..exceptions import ComponentError, ConfigError
from ..conf import TASK_STORAGES

class ProductCompliant(FlowComponent):
    """
        ProductCompliant

        Overview

            The ProductCompliant class is a component for interacting with an IA Agent for making Customer Satisfaction Analysis.
            It extends the FlowComponent class.

        .. table:: Properties
        :widths: auto

            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | Name             | Required | Description                                                                                      |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
            | output_column    |   Yes    | Column for saving the Customer Satisfaction information.                                         |
            +------------------+----------+--------------------------------------------------------------------------------------------------+
        Return

            A Pandas Dataframe with the Customer Satisfaction statistics.

    """ # noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        # System Prompt:
        self.system_prompt = "Product Compliant: "
        self._bot_name = kwargs.get('bot_name', 'CompliantBot')
        # TaskStorage
        # Find in the taskstorage, the "prompts" directory.
        prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        if not prompt_path.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompts Path Not Found: {prompt_path}"
            )
        self.prompt_path = prompt_path
        # is hardcoded to this particular Bot.
        self.system_prompt_file = 'compliantbot.txt'
        # Bot Object:
        self._bot: Any = None

    async def start(self, **kwargs):
        """
            start

            Overview

                The start method is a method for starting the ProductCompliant component.

            Parameters

                kwargs: dict
                    A dictionary containing the parameters for the ProductCompliant component.

            Return

                True if the ProductCompliant component started successfully.

        """
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "CompliantBot: Data Was Not Found"
            )
        if not self.output_column:
            raise ConfigError(
                "ProductCompliant: output_column is required"
            )
        # check if Prompt File exists
        prompt_file = self.prompt_path.joinpath(self.system_prompt_file)
        if not prompt_file.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompt File Not Found: {prompt_file}"
            )
        self.system_prompt_file = prompt_file.name
        # read the prompt file as text:
        with open(prompt_file, 'r') as f:
            self.system_prompt = f.read()
        # Set the Bot:
        try:
            self._bot = BasicBot(
                name=self._bot_name,
                system_prompt=self.system_prompt,
                goal="Your task is to provide a concise and insightful analysis on negative reviews of products",
                use_llm=self.llm.get('name', 'name'),
                model_name=self.llm.get('model_name', 'gemini-2.0-pro'),
            )
            # configure the bot:
            await self._bot.configure()
        except Exception as err:
            raise ComponentError(
                f"{self.system_prompt} Error Configuring Bot: {err}"
            ) from err
        return True

    def format_question(self, product_name, reviews):
        question = f"""
            Product: {product_name}

            Question:
            "What are the primary customer concerns, problems, and issues based on these negative product reviews for {product_name}?"

            Negative Customer Reviews:

        """
        for review in reviews:
            question += f"* {review}\n"
        return question

    async def run(self):
        """
            run

            Overview

                The run method is a method for running the ProductCompliant component.

            Return

                A Pandas Dataframe with the Product Compliant statistics.

        """
        # Group reviews by product_name and aggregate them into a list
        grouped = self.data.groupby(self.product_column)[self.review_column].apply(list).reset_index()
        products_evaluation = {}
        for _, row in grouped.iterrows():
            product_name = row[self.product_column]
            reviews = row[self.review_column]
            formatted_question = self.format_question(product_name, reviews)
            result = await self._bot.question(
                question=formatted_question,
                return_docs=False
            )
            products_evaluation[product_name] = {
                "answer": result.answer
            }
        # Then, create a dataframe only with the columns in "self.columns" grouped.
        grouped_df = self.data.groupby(self.columns).agg(
            num_reviews=(self.review_column, "count"),
            avg_rating=("rating", "mean")
        ).reset_index()
        # Add the Product Compliant column, using the dictionary and match per product_name column
        grouped_df[self.output_column] = grouped_df[self.product_column].map(
            lambda x: products_evaluation[x]['answer']
        )
        # return the grouped dataframe
        self._result = grouped_df
        return self._result

    async def close(self):
        pass
