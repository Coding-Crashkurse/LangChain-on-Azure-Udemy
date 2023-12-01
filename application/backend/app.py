from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from fastapi import FastAPI, UploadFile, File
from azure.storage.blob import BlobServiceClient
import os
from fastapi import FastAPI, HTTPException
from langchain.schema import Document
from langchain.indexes import SQLRecordManager, index


load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn_str = os.getenv("BLOB_CONN_STRING")
container_name = os.getenv("BLOB_CONTAINER")
blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)

host = os.getenv("PG_VECTOR_HOST")
user = os.getenv("PG_VECTOR_USER")
password = os.getenv("PG_VECTOR_PASSWORD")
COLLECTION_NAME = os.getenv("PG_COLLECTION_NAME")
CONNECTION_STRING = (
    f"postgresql+psycopg2://{user}:{password}@{host}:5432/{COLLECTION_NAME}"
)

namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(namespace, db_url=CONNECTION_STRING)

embeddings = OpenAIEmbeddings()

vector_store = PGVector(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    conversation: list[Message]


def format_history(conversation: Conversation) -> str:
    return "\n".join(f"{msg.role}: {msg.content}" for msg in conversation.conversation)


def format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.
{context}
History:
{history}
Question: {question}
Helpful Answer:"""
rag_prompt_custom = PromptTemplate.from_template(template)

embeddings = OpenAIEmbeddings()
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME = "vectordb"
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)
retriever = store.as_retriever()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
rag_chain = (
    {
        "context": retriever | format_docs,
        "history": RunnablePassthrough(),
        "question": RunnablePassthrough(),
    }
    | rag_prompt_custom
    | llm
    | StrOutputParser()
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/conversation")
async def ask_question(question: str, conversation: Conversation) -> dict:
    history_formatted = format_history(conversation)
    answer = rag_chain.invoke({"question": question, "history": history_formatted})
    return {"answer": answer}


@app.post("/uploadfiles/")
async def upload_files(files: list[UploadFile] = File(...)):
    container_client = blob_service_client.get_container_client(container_name)
    uploaded_files = []

    for file in files:
        blob_client = container_client.get_blob_client(blob=file.filename)

        contents = await file.read()
        blob_client.upload_blob(contents, overwrite=True)
        uploaded_files.append(file.filename)

    return {"uploaded_files": uploaded_files}


@app.post("/index_documents/")
async def index_documents(documents: list[Document]):
    try:
        result = index(
            documents,
            record_manager,
            vector_store,
            cleanup="full",
            source_id_key="source",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
