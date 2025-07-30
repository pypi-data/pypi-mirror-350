
from enum import Enum
from typing import List, Any
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore


import faiss

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore

from pinecone import Pinecone
from pinecone import ServerlessSpec




class VectorStoreType(Enum):
    SimpleVectorStore = 'SimpleVectorStore'
    FAISS = 'FAISS'
    PINECONE = "PINECONE"
    # 添加更多选项

class VectorStore:
    def __new__(cls, type: VectorStoreType) -> Any:
        assert type.value in [i.value for i in VectorStoreType]
        instance = None

        if type.value == 'SimpleVectorStore':
            instance = SimpleVectorStore()

        elif type.value == 'FAISS':
            # Create a FAISS index
            faiss_index = faiss.IndexFlatL2(1536)  # Example dimension
            instance = FaissVectorStore(faiss_index=faiss_index)

        elif type.value == 'PINECONE':
            # Create a FAISS index
            api_key = os.environ["PINECONE_API_KEY"]
            pc = Pinecone(api_key=api_key)
            pinecone_index = pc.Index("quickstart-index")
            vector_store = PineconeVectorStore(
                                            pinecone_index=pinecone_index, namespace="test_05_14"
                                        )
            instance = vector_store


        else:
            raise Exception('Unknown type')

        return instance


class DocStoreType(Enum):
    SimpleDocumentStore = 'SimpleDocumentStore'
    # Add more options as needed


class DocStore:
    def __new__(cls, type: DocStoreType) -> Any:
        assert type.value in [i.value for i in DocStoreType]
        instance = None

        if type.value == 'SimpleDocumentStore':
            instance = SimpleDocumentStore()
            
        else:
            raise Exception('Unknown type')

        return instance


class GraphStoreType(Enum):
    SimpleGraphStore = 'SimpleGraphStore'
    NebulaGraphStore = 'NebulaGraphStore'
    Neo4jGraphStore = 'Neo4jGraphStore'
    MemgraphGraphStore = 'MemgraphGraphStore'

class GraphStore:
    def __new__(cls, type: GraphStoreType) -> Any:
        assert type.value in [i.value for i in GraphStoreType]
        instance = None

        if type.value == 'SimpleGraphStore':
            instance = SimpleGraphStore()
        
        elif type.value == 'NebulaGraphStore':
            from llama_index.graph_stores.nebula import NebulaPropertyGraphStore
            # Initialize NebulaPropertyGraphStore
            graph_store = NebulaPropertyGraphStore(
                space="llamaindex_nebula_property_graph",
                overwrite=True  # Overwrite existing space if needed
            )
            instance = graph_store


        elif type.value == 'Neo4jGraphStore':
            from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

            graph_store = Neo4jPropertyGraphStore(
                username="neo4j",
                password="llamaindex",
                url="bolt://localhost:7687",
            )
            instance = graph_store

        elif type.value == 'MemgraphGraphStore':
            from llama_index.graph_stores.memgraph import MemgraphPropertyGraphStore

            graph_store = MemgraphPropertyGraphStore(
                username="",# Enter your Memgraph username (default "")
                password="",# Enter your Memgraph password (default "")
                url="",  # Specify the connection URL, e.g., 'bolt://localhost:7687'
            )
            instance = graph_store
        else:
            raise Exception('Unknown type')

        return instance



