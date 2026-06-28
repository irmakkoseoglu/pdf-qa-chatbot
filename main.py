#The stack that will be used are ollama TinyLlama (local), langchain, chromadb, and fastapi, docker.
#First let's create a virtual environment and install the required packages.
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import io
from pydantic import BaseModel


#pdf file querying inside of the prompt, we will use the PyPDF2 library to read the pdf file and extract the text from it. Then we will use the langchain library to create a vector store using chromadb and then we will use the ollama to query the vector store and get the answer from the pdf file.


#Read the pdf file and extract the text from it.
def read_pdf(pdf_bytes: bytes) -> str:
    pdf_text = ""
    pdf_reader= PdfReader(io.BytesIO(pdf_bytes))
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

#split the text into chunks using the langchain library.
def split_text_into_chunks(pdf_text: str) -> list:
    pdf_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200, #overlapping the text in the chunks to prevent data loss
    length_function= len,
    separators= ["\n\n", "\n", " ", ""]
    )
    return pdf_text_splitter.split_text(text= pdf_text)

#the chunks will be vector embedded with the huggingface embedding model.this vector embeddings understands the semantic meaning of the text and can be used to query the text in a more efficient way.
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

#the vector store will be created using the chromadb library and the chunks will be added to the vector store.
vector_store = None
def vector_storage(chunks: list) -> Chroma:
    global vector_store
    if vector_store is None:
        vector_store = Chroma.from_texts(chunks, embedding=embeddings)
    else:
        vector_store.add_texts(chunks, embedding=embeddings)

#query the vector store using the ollama local to get the answer from the pdf file.
def query_vector_store(query: str) -> str:
    if vector_store is None:
        return "Vector store is empty. Please upload a PDF file first."
    
    #retrieve the vector store.
    retreiver = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=Ollama(model="tinyllama"),
        chain_type="stuff",
        retriever=retreiver,
        return_source_documents=True
    )
    result = qa_chain.invoke({"query": query})
    return result["result"]

#main

#checking if the fastapi server is running.
app = FastAPI()
@app.get("/")
def check():
    return {"message": "Hello, this is a PDF QA chatbot using Ollama!"}

#sending the pdf file to the server.
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a PDF file."})
    
    pdf_bytes = await file.read()
    pdf_text = read_pdf(pdf_bytes)
    chunks = split_text_into_chunks(pdf_text)
    vector_storage(chunks)
    
    return JSONResponse(status_code=200, content={"message": "PDF file uploaded and processed successfully."})
#sending the query and getting the answer from the pdf file using the ollama local
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_pdf(request: QueryRequest):
    answer = query_vector_store(request.query)
    return JSONResponse(status_code=200, content={"answer": str(answer)})