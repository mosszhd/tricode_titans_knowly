import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
import os
import shutil


class ChromadbOperations:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str('vectorstore'))
        self.collection = self.client.get_or_create_collection(name="text_collection",
                                                               embedding_function=ONNXMiniLM_L6_V2()) 

    def insert_data(self, texts_chunks):
        embedding_count = len(self.collection.get()['ids'])
        if embedding_count == 0:
            ids = [str(i) for i in range(1, len(texts_chunks)+1)]
        else:
            ids = [str(i) for i in range(embedding_count+1, embedding_count+1+len(texts_chunks))]
        self.collection.add(documents=texts_chunks, ids=ids)

    def count(self):
        return self.collection.count()
    
    def query(self, query_text, k):
        response = self.collection.query(query_texts=[query_text], n_results=k)
        return response['documents'][0]
    
    def delete_vector_storage(self):
        if len(self.client.list_collections()) != 0:
            database_contents = os.listdir(f"{os.getcwd()}/vectorstore")
            self.client.delete_collection(name="text_collection")
            for name in database_contents:
                if os.path.isdir(f"vectorstore/{name}"):
                    shutil.rmtree(f"vectorstore/{name}")
                else:
                    os.remove(f"vectorstore/{name}")