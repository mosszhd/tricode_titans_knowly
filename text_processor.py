from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_document_chunks(path):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n"],
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len
    )

    all_chunks = []

    # loading all pdf documents at once
    pdf_loader = DirectoryLoader(path=str(path), glob="**/*.pdf")
    pdf_documents = pdf_loader.load()
    for single_chunk in  text_splitter.split_documents(documents=pdf_documents):
        all_chunks.append(single_chunk.page_content)

    return all_chunks