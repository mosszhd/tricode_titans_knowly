from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from prompt_templates import templates
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# function for splitting documents into smaller chunks
def get_document_chunks(path):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=config["text_processing"]["separators"],
        chunk_size=config["text_processing"]["chunk_size"],
        chunk_overlap=config["text_processing"]["chunk_overlap"],
        length_function=len
    )

    all_chunks = []

    pdf_loader = DirectoryLoader(path=str(path), glob="**/*.pdf")
    pdf_documents = pdf_loader.load()

    for single_chunk in  text_splitter.split_documents(documents=pdf_documents):
        all_chunks.append(single_chunk)

    return all_chunks

# function for generating embedding from text chunks
def create_vectorstore(chunks: list[Document]):
    vector_db = Chroma.from_documents(documents=chunks,
                                      embedding=OllamaEmbeddings(model=config["vector_db"]["ollama_embeddibg_path"]),
                                      persist_directory=config["vector_db"]["persist_directory"])
    return vector_db

# function for retrieving k numbers of compressed context
def get_compressed_retriever(llm, vector_db, k):
    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, 
                                                           base_retriever=vector_db.as_retriever(search_type="mmr", 
                                                                                                 search_kwargs={"k": k}))
    return compression_retriever

class ragChain:
    def __init__(self, llm, chat_history, retriever):
        self.memory = ConversationBufferMemory(memory_key="chat_history",
                                               return_messages=True)
        self.messages = [SystemMessagePromptTemplate.from_template(templates["rag_prompt"]["system_prompt"]),
                         HumanMessagePromptTemplate.from_template(templates["rag_prompt"]["user_prompt"])]
        self.qa_prompt = ChatPromptTemplate.from_messages(self.messages)
        self.qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                                        retriever=retriever,
                                                        memory=self.memory,
                                                        combine_docs_chain_kwargs={"prompt": self.qa_prompt})
    
    def run(self, query):
        return self.qa({"question": query})["answer"]
