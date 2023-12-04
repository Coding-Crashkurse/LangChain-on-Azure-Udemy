from fastapi import FastAPI
from pydantic import BaseModel
# from dotenv import load_dotenv, find_dotenv
# from langchain.chat_models import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
# from langchain.prompts import PromptTemplate
import logging
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores.pgvector import PGVector
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import RunnablePassthrough
# from fastapi import UploadFile, File
# from azure.storage.blob import BlobServiceClient
# import os
# from fastapi import HTTPException
# from langchain.schema import Document
# from langchain.indexes import SQLRecordManager, index

# load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# conn_str = os.getenv("BLOB_CONN_STRING")
# container_name = os.getenv("BLOB_CONTAINER")
# blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)

# host = os.getenv("PG_VECTOR_HOST")
# user = os.getenv("PG_VECTOR_USER")
# password = os.getenv("PG_VECTOR_PASSWORD")
# COLLECTION_NAME = os.getenv("PG_COLLECTION_NAME")
# CONNECTION_STRING = (
#     f"postgresql+psycopg2://{user}:{password}@{host}:5432/{COLLECTION_NAME}"
# )

# namespace = f"pgvector/{COLLECTION_NAME}"
# record_manager = SQLRecordManager(namespace, db_url=CONNECTION_STRING)

# embeddings = OpenAIEmbeddings()

# vector_store = PGVector(
#     embedding_function=embeddings,
#     collection_name=COLLECTION_NAME,
#     connection_string=CONNECTION_STRING,
# )

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    question: str
    conversation: list[Message]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/conversation")
async def ask_question(conversation: Conversation) -> dict:
    print("Frage:", conversation.question)
    print("Konversation:", conversation.conversation)
    # Fügen Sie hier Ihre Logik zur Verarbeitung der Konversation hinzu
    # Zum Beispiel:
    # history_formatted = format_history(conversation.conversation)
    # answer = rag_chain.invoke({"question": conversation.question, "history": history_formatted})
    # return {"answer": answer}
    return {"response": "Endpoint currently under construction."}



# @app.post("/uploadfiles/")
# async def upload_files(files: list[UploadFile] = File(...)):
#     container_client = blob_service_client.get_container_client(container_name)
#     uploaded_files = []

#     for file in files:
#         blob_client = container_client.get_blob_client(blob=file.filename)

#         contents = await file.read()
#         blob_client.upload_blob(contents, overwrite=True)
#         uploaded_files.append(file.filename)

#     return {"uploaded_files": uploaded_files}


# @app.post("/index_documents/")
# async def index_documents(documents: list[Document]):
#     try:
#         result = index(
#             documents,
#             record_manager,
#             vector_store,
#             cleanup="full",
#             source_id_key="source",
#         )
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
