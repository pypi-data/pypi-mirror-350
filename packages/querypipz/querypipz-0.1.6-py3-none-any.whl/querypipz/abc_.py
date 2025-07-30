
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from typing import List, Dict, Optional


class QueryerABC():
    def __init__(self):
        self.persist_path = None
        self.reader: Optional[SimpleDirectoryReader] = None
        self.ingestion_pipeline: Optional[IngestionPipeline] = None
        self.storage_context = None
        self.index_type = None
        self.retriever_Nest = None  # Type hint will be added later
        self.query_pipeline = None  # Type hint will be added later

    def build(self):
        pass
    
    def query(self, prompt: str, similarity_top_k: int = 3):
        pass

    def retrieve(self, query_text: str, similarity_top_k: int = 5):
        pass


# 生成器接口
class QueryBuilder:

    def set_llm(self):
        pass

    def build_reader(self):
        pass

    def build_ingestion_pipeline(self):
        pass

    def build_storage_context(self):
        pass

    def build_index(self):
        pass

    def build_retriver(self):
        pass

    def build_query_pipeline(self):
        pass

    def get_queryer(self):
        pass

    def build_tools(self):
        pass

    def build_kg_extractors(self):
        pass