"""
The Main module that takes a query as a console argument and returns answer depending on the context,
retrieved from the vector database.
"""
import argparse
import logging

from langchain_chroma import Chroma
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from setup_logging import setup_logging
from embedding_function import get_embedding_function
from config import DB_PATH, PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def main():
    """
    Parses query from console and outputs the response from the model
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The question you would like to ask.")
    args = parser.parse_args()
    query_text = args.query_text

    response_text = query_rag(query_text)
    logger.info(response_text)


def query_rag(query: str):
    """
    Retrieves relevant documents to the given query and gets a query response from
    OpenAI chat model based on the context which is formed from the relevant chunks.
    :param query:
    :return:
    """
    chroma = Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_function()
    )
    relevant_chunks = chroma.similarity_search_with_relevance_scores(query=query, k=4)

    context = "\n\n---\n\n".join([chunk.page_content for chunk, _ in relevant_chunks])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=query)

    model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
    response = model.invoke(prompt)

    sources_with_scores = "; ".join([f"{chunk.metadata.get('id')}: {score: .2f}"
                                     for chunk, score in relevant_chunks])

    response_text = f"Відповідь: {response.content}\n\nДжерела: {sources_with_scores}"

    return response_text


if __name__ == "__main__":
    setup_logging()
    main()
