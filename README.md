# PDF RAG

This is just a simple console RAG for retrieving information from PDFs that you load into `data` folder. It uses 
OpenAI's `text-embedding-3-small` embedding model and `gpt-4o-mini-2024-07-18` chat model. 

## Deployment

You should create `.env` file with OpenAI API Key, and paths for data and vector db's persistent folders. 
The example lies in ``