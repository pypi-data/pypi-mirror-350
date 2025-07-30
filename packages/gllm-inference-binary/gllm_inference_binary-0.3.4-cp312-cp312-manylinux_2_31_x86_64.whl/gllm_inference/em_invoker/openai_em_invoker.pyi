from gllm_inference.em_invoker.langchain_em_invoker import LangChainEMInvoker as LangChainEMInvoker
from typing import Any

class OpenAIEMInvoker(LangChainEMInvoker):
    """An embedding model invoker to interact with embedding models hosted through OpenAI API endpoints.

    The `OpenAIEMInvoker` class is responsible for invoking an embedding model using the OpenAI API.
    It uses the embedding model to transform a text or a list of input text into their vector representations.

    Attributes:
        em (OpenAIEmbeddings): The embedding model instance to interact with OpenAI models.
    """
    def __init__(self, model_name: str, api_key: str, model_kwargs: Any = None) -> None:
        """Initializes a new instance of the OpenAIEMInvoker class.

        Args:
            model_name (str): The name of the OpenAI model to be used.
            api_key (str): The API key for accessing the OpenAI model.
            model_kwargs (Any, optional): Additional keyword arguments to initiate the OpenAI model. Defaults to None.
        """
