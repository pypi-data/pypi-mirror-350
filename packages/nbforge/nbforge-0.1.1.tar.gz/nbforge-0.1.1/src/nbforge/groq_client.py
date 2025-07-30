import os
from langchain_groq import ChatGroq
from nbforge.logger import setup_logger

logger = setup_logger(__name__)


class GroqClient:
    """
    Manages the instantiation and configuration of a ChatGroq language model client.
    """

    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initializes the GroqClient with the specified API key and model.

        Args:
            api_key (str, optional): The API key for Groq. If not provided, uses the GROQ_API_KEY environment variable.
            model (str, optional): The model name to use. Defaults to "llama-3.3-70b-versatile".

        Returns:
            None

        Raises:
            ValueError: If no API key is provided or found in the environment.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it in the environment variables."
            )

        self.llm = ChatGroq(model=self.model, temperature=0, groq_api_key=self.api_key)

    def get_model(self):
        """
        Returns the ChatGroq model instance.

        Args:
            None

        Returns:
            ChatGroq: The instantiated ChatGroq model object.
        """
        return self.llm
