from enum import Enum
from typing import List, Any

from pinecone import Pinecone
from pinecone import ServerlessSpec
from pinecone.data.index import Index
from llama_index.core import StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.vector_stores.postgres import PGVectorStore
import os
from enum import Enum



class Pineconer():
    def __init__(self,api_key = None):
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=self.api_key)

    def create(self,index_name:str):
        self.pc.create_index(
            index_name,#"api-documents-index",
            dimension=1536, # 维度1536
            metric="euclidean",#欧式空间 "cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    
    def load(self)->Index:
        pinecone_index = self.pc.Index("api-documents-index")
        return pinecone_index
    
    def get_storage(self,pinecone_index:Index)->StorageContext:
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index,namespace = "test1")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context



class PGVector():
    def __init__(self,info = None):
        self.info = info

    def create(self):
        pass

    
    def load(self):
        pass
    
    def get_storage(self,index_name:str)->StorageContext:
        vector_store = PGVectorStore.from_params(
            database="vector_db",
            host=self.info.host,
            password=self.info.password,
            port=self.info.port,
            user=self.info.user,
            table_name=index_name,
            embed_dim=1536,  # openai embedding dimension
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
                },
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context







class IndexType(Enum):
    PineconeVectorStore = 'PineconeVectorStore'
    PGVector = 'PGVector'
    ChromaVectorStore = 'ChromaVectorStore'
    # 添加更多选项

class Indexs:# 配合store 
    def __new__(cls, type: IndexType) -> Any:
        assert type.value in [i.value for i in IndexType]
        instance = None

        if type.value == 'PineconeVectorStore':
            instance = Pineconer()
            # instance = SomeClass(param1=value1, param2=value2)
            instance.create(index_name='1234')
            instance = instance.load()


        elif type.value == 'PGVector':
            instance = PGVector()
            # instance = AnotherClass(param1=value1, param2=value2)

        elif type.value == 'ChromaVectorStore':
            instance = PGVector()
            import chromadb
            from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
            from llama_index.vector_stores.chroma import ChromaVectorStore
            from llama_index.core import StorageContext


            # initialize client, setting path to save data
            db = chromadb.PersistentClient(path="./chroma_db")

            # create collection
            chroma_collection = db.get_or_create_collection("quickstart")

            # assign chroma as the vector_store to the context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            # create your index
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )

            # create a query engine and query
            query_engine = index.as_query_engine()
            response = query_engine.query("What is the meaning of life?")
            print(response)
            # instance = AnotherClass(param1=value1, param2=value2)
        else:
            raise Exception('Unknown type')

        return instance


