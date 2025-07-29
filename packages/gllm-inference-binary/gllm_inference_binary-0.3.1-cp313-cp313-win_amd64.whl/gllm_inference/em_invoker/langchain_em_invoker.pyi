from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from langchain_core.embeddings import Embeddings as Embeddings

class LangChainEMInvoker(BaseEMInvoker):
    """An embedding model invoker to interact with embedding models defined using LangChain's Embeddings.

    The `LangChainEMInvoker` class is responsible for invoking an embedding model defined using LangChain's
    Embeddings module. It uses the embedding model to transform the input text or list of texts into their
    vector representations.

    Attributes:
        em (Embeddings): The instance to interact with an embedding model defined using LangChain's Embeddings.
    """
    em: Incomplete
    def __init__(self, em: Embeddings) -> None:
        """Initializes a new instance of the LangChainEMInvoker class.

        Args:
            em (Embeddings): The instance to interact with an embedding model defined using LangChain's Embeddings.
        """
    async def invoke(self, text: str | list[str]) -> list[float] | list[list[float]]:
        """Invokes the LangChain embedding model with the provided text or list of texts.

        Args:
            text (str | list[str]): The input text or list of texts to be embedded using the embedding model.

        Returns:
            list[float] | list[list[float]]: The vector representations of the input text:
                1. If the input is a string, the output is a `list[float]`.
                2. If the input is a list of strings, the output is a `list[list[float]]`.
        """
    def to_langchain(self) -> Embeddings:
        """Converts the current embedding model invoker to an instance of LangChain `Embeddings` object.

        Returns:
            Embeddings: An instance of LangChain `Embeddings` object.
        """
