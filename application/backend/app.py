import logging
import os
from operator import itemgetter

from azure.storage.blob import BlobServiceClient
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import Document, StrOutputParser, format_document
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.vectorstores.pgvector import PGVector
from pydantic import BaseModel, Field

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
record_manager.create_schema()

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


class DocumentIn(BaseModel):
    page_content: str
    metadata: dict = Field(default_factory=dict)


def _format_chat_history(conversation: list[Message]) -> str:
    formatted_history = ""
    for message in conversation:
        formatted_history += f"{message.role}: {message.content}\n"
    return formatted_history.rstrip()


def format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


embeddings = OpenAIEmbeddings()
COLLECTION_NAME = "vectordb"
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)
retriever = store.as_retriever()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

condense_question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question_template)

answer_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""


ANSWER_PROMPT = ChatPromptTemplate.from_template(answer_template)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


_inputs = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | llm
    | StrOutputParser(),
)

_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}
conversational_qa_chain = (
    _inputs | _context | ANSWER_PROMPT | ChatOpenAI() | StrOutputParser()
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
    answer = conversational_qa_chain.invoke(
        {"question": question, "chat_history": conversation.conversation}
    )
    print(answer)
    return {"answer": answer}

@app.get("/listfiles")
async def list_files(page: int = 1, page_size: int = 10):
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    files = [blob.name for blob in blob_list]
    total_files = len(files)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "total_files": total_files,
        "files": files[start:end],
        "page": page,
        "total_pages": (total_files - 1) // page_size + 1,
    }


@app.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob=filename)

    try:
        blob_client.delete_blob()
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


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
async def index_documents(documents_in: list[DocumentIn]):
    print(documents_in)
    try:
        documents = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in documents_in
        ]
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
