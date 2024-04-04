from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def get_document_chunks(path):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=config["text_split"]["separators"],
        chunk_size=config["text_split"]["chunk_size"],
        chunk_overlap=config["text_split"]["chunk_overlap"],
        length_function=len
    )

    all_chunks = []

    # loading all pdf documents at once
    pdf_loader = DirectoryLoader(path=str(path), glob="**/*.pdf")
    pdf_documents = pdf_loader.load()
    for single_chunk in  text_splitter.split_documents(documents=pdf_documents):
        all_chunks.append(single_chunk.page_content)

    return all_chunks