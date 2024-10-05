from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore 
from pinecone import Pinecone, ServerlessSpec
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import random
import string
import os

# split your document into chunks
def load_and_split_docs(path): 
    loader = PyPDFLoader(path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
    )
    docs = loader.load_and_split(text_splitter)
    return docs

# create embeddings from the documents and upsert them to pinecone
def upsert_to_pinecone(docs, index_name):
    model = "sentence-transformers/all-mpnet-base-v2"
    HUGGGINGFACEHUB_API_KEY = os.getenv("HUGGGINGFACEHUB_API_KEY")
    # create embeddings from the documents
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",
        huggingfacehub_api_token= HUGGGINGFACEHUB_API_KEY,
    )
    print(embeddings)

    PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
    pc = Pinecone(PINECONE_API_KEY)

    indexes = [index.name for index in pc.list_indexes()]
    if index_name not in indexes:
        pc.create_index(name=index_name, dimension=768, metric="cosine", spec= ServerlessSpec(cloud = 'aws', region = "us-east-1"))

    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index, embeddings)
    vector_store.add_documents(docs)
    return vector_store

# create retrieval chain 
def create_chain(vector_store):
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
    return chain

def random_string():
    char_set = string.ascii_lowercase
    return  ''.join(random.sample(char_set*6, 6))
