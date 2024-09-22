"""
Module for retrieving the embedding function.
"""
from langchain_openai import OpenAIEmbeddings


def get_embedding_function(model: str = "text-embedding-3-small"):
    """
    Returns the embedding function for the given OpenAI embedding model.
    :param model: Model name
    :return: embedding function
    """
    embedding_function = OpenAIEmbeddings(model=model)

    return embedding_function
