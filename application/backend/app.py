from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.schema import StrOutputParser, RunnablePassthrough

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
