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
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from operator import itemgetter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.indexes import SQLRecordManager
from langchain.chains import RetrievalQA
from langchain.schema import format_document
from langchain.schema.runnable import RunnableParallel
from langchain.prompts import ChatPromptTemplate


from langchain.schema import Document

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



# Define the templates
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
conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | ChatOpenAI() | StrOutputParser()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import Request
import json


@app.post("/conversation")
async def ask_question(question: str, conversation: Conversation) -> dict:
    print(f"Received Question: {question}")
    print(f"Received Conversation: {conversation}")

    answer = conversational_qa_chain.invoke({"question": question, "chat_history": conversation.conversation})
    print(answer)
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

from pydantic import BaseModel, Field
from typing import Dict, List

class DocumentIn(BaseModel):
    page_content: str
    metadata: Dict = Field(default_factory=dict)


from fastapi import HTTPException
from langchain.schema import Document  # Import the Langchain Document class

@app.post("/index_documents/")
async def index_documents(documents_in: List[DocumentIn]):
    print(documents_in)
    try:
        # Convert Pydantic objects to Langchain Document objects
        documents = [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in documents_in]

        # Proceed with indexing using Langchain Document objects
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


@app.post("/index_documents_test/")
async def index_documents(request: Request):
    raw_data = await request.json()  # Get raw JSON data
    print(raw_data)  # Log it for debugging