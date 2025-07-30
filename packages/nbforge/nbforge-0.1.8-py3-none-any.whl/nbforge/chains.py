import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from nbforge.groq_client import GroqClient
from dotenv import load_dotenv
import yaml
from utils.constants import *
import platform
from nbforge.logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)


class Chains:
    """
    Handles the conversion of notebook blocks into a structured Python project using language model prompts.
    """

    def __init__(self):
        """
        Initializes the Chains object by loading the language model and prompts.

        Args:
            None

        Returns:
            None
        """
        self.llm = GroqClient().get_model()
        self.prompts = self.load_prompts("src/nbforge/utils/prompts.yml")

    @staticmethod
    def load_prompts(file_path):
        """
        Loads prompts from a YAML file.

        Args:
            file_path (str): Path to the YAML file containing prompts.

        Returns:
            dict: Dictionary of prompts loaded from the file.
        """
        with open(file_path, "r") as file:
            prompts = yaml.safe_load(file)
        return prompts

    def get_prompt(self, key):
        """
        Fetches a specific prompt by key.

        Args:
            key (str): The key for the desired prompt.

        Returns:
            str: The prompt template string.

        Raises:
            Exception: If the key is not found in the prompts.
        """
        if key not in self.prompts:
            raise Exception(f"Prompt '{key}' not found in prompts.yml")
        return self.prompts[key]

    def get_file_structure(
        self, code_blocks, markdown_blocks, streamlit_desc_block, fastAPI_desc_block
    ):
        """
        Generates the file structure for the Python project based on notebook blocks and special description blocks.

        Args:
            code_blocks (list): List of code cell sources.
            markdown_blocks (list): List of markdown cell sources.
            streamlit_desc_block (str or None): Streamlit description block if present, else None.
            fastAPI_desc_block (str or None): FastAPI description block if present, else None.

        Returns:
            list: List of dictionaries, each containing 'fileName' and 'fileContent' for the generated files.

        Raises:
            OutputParserException: If the response cannot be parsed as JSON.
        """
        prompt_name = None
        if streamlit_desc_block is not None:
            prompt_name = NB_TO_MODULE_STREAMLIT_PROMPT
        elif fastAPI_desc_block is not None:
            prompt_name = NB_TO_MODULE_FASTAPI_PROMPT
        else:
            prompt_name = NB_TO_MODULE_PROMPT
        prompt_file_structure = PromptTemplate.from_template(
            self.get_prompt(prompt_name)
        )
        chain_extract = prompt_file_structure | self.llm
        res = chain_extract.invoke(
            input={
                "code_blocks": code_blocks,
                "markdown_blocks": markdown_blocks,
                "streamlit_desc_block": streamlit_desc_block,
                "fastAPI_desc_block": fastAPI_desc_block,
                "platform": platform.system(),
            }
        )
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            logger.error("Context too big. Unable to parse data.")
            raise OutputParserException("Context too big. Unable to parse data.")
        return res
