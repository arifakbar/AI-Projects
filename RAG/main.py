import os
import glob
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import gradio as gr

from prompts import system_prompt


load_dotenv()

model_name = "qwen/qwen3-32b"
db_name = "vector_db"

#Checking the number of documents in the knowledge base

docs = glob.glob("knowledge-base/*", recursive=True)
print(f"Total docs: {len(docs)}")

#Loading Files from the knowledge base

loader = DirectoryLoader(
    "./knowledge-base",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

files = loader.load()

#Splitting the files into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(files)

print(f"Total chunks: {len(chunks)}")

#Making the embeddings and storing them in the vector database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists("vector_db"):
    print("Vector database already exists.")
else:
    print("Creating vector database...")
    vector_db = Chroma.from_documents(chunks, embeddings, collection_name=db_name)

#Retrieving the vector database
retriever = vector_db.as_retriever()
llm = ChatGroq(model=model_name, reasoning_format="parsed")

def qna(q:str,history):
  docs = retriever.invoke(q)
  c = "\n\n".join(d.page_content for d in docs)
  sys_prompt = system_prompt.format(context=c)
  res = llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=q)])
  return res.content

gr.ChatInterface(qna).launch()
