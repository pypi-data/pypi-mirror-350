import abc
from abc import ABC, abstractmethod
from langchain_core.embeddings import Embeddings as Embeddings

class BaseEMInvoker(ABC, metaclass=abc.ABCMeta):
    """A base class for embedding model invokers used in Gen AI applications.

    The `BaseEMInvoker` class provides a framework for invoking embedding models.

    Attributes:
        None
    """
    @abstractmethod
    async def invoke(self, text: str | list[str]) -> list[float] | list[list[float]]:
        """Invokes the embedding model with the provided text or list of texts.

        This abstract method must be implemented by subclasses to define the logic for invoking the embedding model.
        It uses the embedding model to transform the input text or list of texts into their vector representations.

        Args:
            text (str | list[str]): The input text or list of texts to be embedded using the embedding model.

        Returns:
            list[float] | list[list[float]]: The vector representations of the input text:
                1. If the input is a string, the output is a `list[float]`.
                2. If the input is a list of strings, the output is a `list[list[float]]`.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
    @abstractmethod
    def to_langchain(self) -> Embeddings:
        """Converts the current embedding model invoker to an instance of LangChain `Embeddings` object.

        This abstract method must be implemented by subclasses to define the logic for converting the
        embedding model invoker to an instance of LangChain `Embeddings` object.

        Returns:
            Embeddings: An instance of LangChain `Embeddings` object.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
