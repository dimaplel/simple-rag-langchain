from langchain_openai import OpenAIEmbeddings


def get_embedding_function(model: str = "text-embedding-3-small"):
    embedding_function = OpenAIEmbeddings(model=model)

    return embedding_function
