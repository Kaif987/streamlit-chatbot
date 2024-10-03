from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore 
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

load_dotenv()

# split your document into chunks
def load_and_split_docs(): 
    loader = PyPDFLoader("./attention.pdf")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
    )
    docs = loader.load_and_split(text_splitter)
    return docs

# create embeddings from the documents and upsert them to pinecone
def upsert_to_pinecone(docs):
    model = "sentence-transformers/all-mpnet-base-v2"
    HUGGGINGFACEHUB_API_KEY = os.getenv("HUGGGINGFACEHUB_API_KEY")
    # create embeddings from the documents
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",
        huggingfacehub_api_token= HUGGGINGFACEHUB_API_KEY,
    )
    PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
    pc = Pinecone(PINECONE_API_KEY)
    index = pc.Index("huggingface-pinecone")
    vector_store = PineconeVectorStore(index, embeddings)
    vector_store.add_documents(docs)
    return vector_store

# create a retrieval chain 

docs = load_and_split_docs()
vector_store = upsert_to_pinecone(docs)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

prompt_template = """
    Answer the question based only on the supplied context. If you don't know the answer, say you don't know the answer.
    Context: {context}
    Question: {question}
    Your answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm 
    | StrOutputParser()
)

# response = chain.invoke("Who is Kaif ?")
# print(response)

