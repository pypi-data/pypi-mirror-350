from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_inference.em_invoker.langchain import TEIEmbeddings as TEIEmbeddings
from gllm_inference.utils import get_basic_auth_headers as get_basic_auth_headers, preprocess_tei_input as preprocess_tei_input

class TEIEMInvoker(BaseEMInvoker):
    """An embedding model invoker to interact with embedding models hosted in Text Embeddings Inference (TEI).

    The `TEIEMInvoker` class is responsible for invoking an embedding model in Text Embeddings Inference (TEI).
    It uses the embedding model to transform a text or a list of input text into their vector representations.

    Attributes:
        client (AsyncInferenceClient): The client instance to interact with the TEI service.
        query_prefix (str): The additional prefix to be added when embedding a query.
        document_prefix (str): The additional prefix to be added when embedding documents.
    """
    client: Incomplete
    query_prefix: Incomplete
    document_prefix: Incomplete
    def __init__(self, url: str, username: str = '', password: str = '', api_key: str | None = None, query_prefix: str = '', document_prefix: str = '') -> None:
        """Initializes a new instance of the TEIEMInvoker class.

        Args:
            url (str): The URL of the TEI service.
            username (str, optional): The username for Basic Authentication. Defaults to an empty string.
            password (str, optional): The password for Basic Authentication. Defaults to an empty string.
            api_key (str | None, optional): The API key for the TEI service. Defaults to None.
            query_prefix (str, optional): The additional prefix to be added when embedding a query.
                Defaults to an empty string.
            document_prefix (str, optional): The additional prefix to be added when embedding documents.
                Defaults to an empty string.
        """
    async def invoke(self, text: str | list[str]) -> list[float] | list[list[float]]:
        """Invokes the embedding model with the provided text or list of texts.

        This method preprocesses the input text and invokes the embedding model to get the vector representations
        of the input text. The prefix used during the preprocessing is determined by the input:
        1. If the input is a single text, the prefix is the `query_prefix`.
        2. If the input is a list of texts, the prefix is the `document_prefix`.

        Args:
            text (str | list[str]): The input text or list of texts to be embedded using the embedding model.

        Returns:
            list[float] | list[list[float]]: The vector representations of the input text:
                1. If the input is a string, the output is a `list[float]`.
                2. If the input is a list of strings, the output is a `list[list[float]]`.
        """
    def to_langchain(self) -> TEIEmbeddings:
        """Converts the current embedding model invoker to an instance of LangChain `TEIEmbeddings` object.

        Returns:
            TEIEmbeddings: An instance of LangChain `TEIEmbeddings` object.
        """
