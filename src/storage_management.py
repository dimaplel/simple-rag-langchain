"""
Module that adds documents from the data folder into the vector db. Each page becomes a separate
document, which has then to be split into chunks for greater granularity. If --clear
argument is present, the vector db is cleared first.
"""
import argparse
import logging
import shutil

from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_PATH, DB_PATH

from embedding_function import get_embedding_function


logger = logging.getLogger(__name__)


def main():
    """
    Method, that loads new documents from the `data` folder into the vector db.
    Parses --clear argument and, if present, clears the vector db.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true", help="Clear all the data from the DB.")
    args = parser.parse_args()
    if args.clear:
        logger.info("🌌 Clearing it up for you!")
        clear_chroma()

    documents = load_from_folder()
    chunks = split_documents(documents)
    add_data_to_chroma(chunks)


def load_from_folder() -> list[Document] or None:
    """
    Loads PDF documents from the data folder
    :return: list of Documents, or None if no documents were loaded
    """
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def split_documents(documents: list[Document]):
    """
    Splits documents into chunks for further storage in the vector db
    :param documents: list of Documents to create chunks from
    :return: chunks, which are fragments of the documents
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=20,
    )
    return splitter.split_documents(documents)


def add_data_to_chroma(chunks: list[Document]):
    """
    Checks if there are new chunks and adds the new ones to the vector db.
    Ids are generated for chunks, and its contents are turned into embeddings and stored there.
    :param chunks: Split documents
    :return: None
    """
    chroma = Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embedding_function()
    )

    chunk_with_ids = generate_document_ids(chunks)
    existing_items = chroma.get(include=[])
    existing_ids = set(existing_items.get("ids"))

    chunk_with_ids = [chunk for chunk in chunk_with_ids
                      if chunk.metadata.get("id") not in existing_ids]

    if chunk_with_ids:
        logger.info("🦜 Adding %i new documents to Chroma" % len(chunk_with_ids))
        new_ids = [chunk.metadata.get("id") for chunk in chunk_with_ids]
        chroma.add_documents(documents=chunk_with_ids, ids=new_ids)
        return

    logger.warning("💾 No new documents were found")


def clear_chroma():
    """
    Clears the Chroma db by deleting the persistent db directory.
    :return: None
    """
    shutil.rmtree(DB_PATH, ignore_errors=True)


def generate_document_ids(chunks: list[Document]):
    """
    Generates id for chunks, so that they could be added into vector db

    :param chunks: Split documents
    :return: chunks with ids based on the source file, page and chunk number.
    Format: `source:page:chunk`
    """
    prev_page = None
    cur_chunk_id = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        cur_page = f"{source}:{page}"

        if prev_page == cur_page:
            cur_chunk_id += 1
        else:
            cur_chunk_id = 0

        chunk_id = f"{cur_page}:{cur_chunk_id}"
        prev_page = cur_page

        chunk.metadata["id"] = chunk_id

    return chunks


if __name__ == "__main__":
    from setup_logging import setup_logging
    setup_logging()
    main()
