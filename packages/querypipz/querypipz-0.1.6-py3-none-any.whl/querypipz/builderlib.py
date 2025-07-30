

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
)


from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex
from typing import List, Dict, Optional
from .abc_ import QueryerABC
from .abc_ import QueryBuilder
from .factory.reader import Reader,ReaderType
from .factory.ingestion_pipeline import Splitter,SplitterType
from .factory.ingestion_pipeline import Cleaner,CleanerType, Embedding, EmbeddingType
from .factory.store import VectorStore,VectorStoreType
import os
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph.transformations import ImplicitPathExtractor,SchemaLLMPathExtractor,SimpleLLMPathExtractor, DynamicLLMPathExtractor


class Queryer(QueryerABC):
    def __init__(self):
        self.persist_path = None
        self.reader: Optional[SimpleDirectoryReader] = None
        self.ingestion_pipeline: Optional[IngestionPipeline] = None
        self.storage_context = None
        self.index_type = None
        self.retriever_Nest = None  # Type hint will be added later
        self.query_pipeline = None  # Type hint will be added later
        self.retriever = None
        self.index: Optional[VectorStoreIndex] = None
        self.kg_extractors = None
        

    def build(self):
        if self.reader is None:
            raise ValueError("Reader is not set. Call build_reader first.")
        
        documents = self.reader.load_data()
        nodes = None
        if self.ingestion_pipeline:
            nodes = self.ingestion_pipeline.run(documents=documents)


        if nodes:
            if self.index_type == "VectorStoreIndex":
                self.index = VectorStoreIndex(nodes,storage_context = self.storage_context)
                # self.index = PropertyGraphIndex(nodes,storage_context = self.storage_context,show_progress=True,)

        else:
            if self.index_type == "VectorStoreIndex":
                self.index = VectorStoreIndex(nodes,storage_context = self.storage_context)

            elif self.index_type == "PropertyGraphIndex":
                self.index = PropertyGraphIndex.from_documents(
                                                            documents=documents,
                                                            show_progress=True,
                                                            kg_extractors = self.kg_extractors,
                                                            # embed_kg_nodes = False,
                                                            )
        return 'builded'

    def get_retriever(self, similarity_top_k: int = 5):
        """
        获取检索器（Retriever），如有必要则从持久化目录加载索引。
        """
        if self.retriever is not None:
            return self.retriever

        if not self.persist_path or not os.path.exists(self.persist_path):
            raise ValueError("索引持久化目录不存在，无法构建检索器。")

        storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
        self.index = load_index_from_storage(storage_context=storage_context)
        self.retriever = self.index.as_retriever(similarity_top_k=similarity_top_k,
                                                 include_text=False,
                                                 )
        return self.retriever

    def retrieve(self, query_text: str, similarity_top_k: int = 5):
        """
        使用检索器进行检索。
        """
        retriever = self.get_retriever(similarity_top_k=similarity_top_k)
        return retriever.retrieve(query_text)

    def get_query_engine(self, similarity_top_k: int = 3):
        """
        获取查询引擎（QueryEngine），如有必要则从持久化目录加载索引。
        """
        if self.query_engine is not None:
            return self.query_engine

        if not self.persist_path or not os.path.exists(self.persist_path):
            raise ValueError("索引持久化目录不存在，无法构建查询引擎。")

        storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
        self.index = load_index_from_storage(storage_context=storage_context)
        self.query_engine = self.index.as_query_engine(similarity_top_k=similarity_top_k,
                                                       include_text=True,)
        return self.query_engine

    def query(self, prompt: str, similarity_top_k: int = 3):
        """
        执行查询。
        """
        query_engine = self.get_query_engine(similarity_top_k=similarity_top_k)
        return query_engine.query(prompt)

# index.property_graph_store.save_networkx_graph(name="./kg3.html") # for debug

class ObsidianDateBuilder(QueryBuilder):
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/date'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/GitHub/obsidian/工作/日记'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path,
                                          file_extractor = {".md": Reader(ReaderType.ObsidianReaderCus)},
                                          recursive=True,
                                          )
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(transformations=[Splitter(SplitterType.TokenTextSplitter),
                                                                           Embedding(EmbeddingType.OpenAIEmbedding),
                                                                           ])

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(vector_store=VectorStore(VectorStoreType.SimpleVectorStore))

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"

    def build_retriver(self):
        self.query.retriever_Nest = None

    def build_query_pipeline(self):
        self.query.query_engine = None
        
    def get_queryer(self):
        return self.query
    
    def build_tools(self):
        pass
    

class ObsidianHabitBuilder(ObsidianDateBuilder):
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/habit'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/GitHub/obsidian/工作/习惯'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path,
                                          file_extractor = {".md": Reader(ReaderType.ObsidianReaderCus)},
                                          recursive=True,
                                          )
    def build_tools(self):
        pass

class DeDaoJYRKBuilder(QueryBuilder):
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/JYRK'):
        self.query = Queryer()
        self.query.persist_path = persist_path

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/work1'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path,
                                          file_extractor = {".md": Reader(ReaderType.PDFFileReader)},
                                          recursive=True,
                                        #   exclude=["*.mp3"],
                                          )
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(transformations=[Cleaner(CleanerType.DeDaoCleaner),
                                                                           Embedding(EmbeddingType.OpenAIEmbedding),
                                                                           ])

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(vector_store=VectorStore(VectorStoreType.FAISS))

    def build_index(self):
        self.query.index_type = "VectorStoreIndex"


    def build_retriver(self):
        self.query.retriever_Nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None
        

    def get_queryer(self):
        return self.query
    
    def build_tools(self):
        pass




class TestGraphBuilder(QueryBuilder):
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph'):
        self.query = Queryer()
        self.query.persist_path = persist_path


    def set_llm(self):
        load_dotenv()
        api_key = os.getenv("BIANXIE_API_KEY")
        api_base = os.getenv("BIANXIE_BASE")
        Settings.llm = OpenAI(model="gpt-4.1",api_base=api_base,api_key=api_key)

    def build_reader(self):
        file_path= '/Users/zhaoxuefeng/本地文稿/百度空间/实验广场/实验/data/chat_history_demo_dongsheng'
        self.query.reader = SimpleDirectoryReader(input_dir=file_path,
                                          file_extractor = {".md": Reader(ReaderType.PDFFileReader)},
                                          recursive=True,
                                        #   exclude=["*.mp3"],
                                          )
    def build_ingestion_pipeline(self):
        self.query.ingestion_pipeline = IngestionPipeline(transformations=[])

    def build_storage_context(self):
        self.query.storage_context = StorageContext.from_defaults(vector_store=VectorStore(VectorStoreType.FAISS))

    def build_index(self):
        self.query.index_type = "PropertyGraphIndex"


    def build_retriver(self):
        self.query.retriever_Nest = None


    def build_query_pipeline(self):
        self.query.query_engine = None
        

    def get_queryer(self):
        return self.query
    
    def build_tools(self):
        def dynamic_method(self, name_path:str):
            return self.index.property_graph_store.save_networkx_graph(name=name_path) # for debug
        self.query.tools = dynamic_method.__get__(self.query,Queryer)



class Test2GraphBuilder(TestGraphBuilder):
    def __init__(self,persist_path='/Users/zhaoxuefeng/GitHub/obsidian/知识库/TestGraph2'):
        self.query = Queryer()
        self.query.persist_path = persist_path
        

    def build_kg_extractors(self):
        self.query.kg_extractors = [SimpleLLMPathExtractor(),
                                    ImplicitPathExtractor(),]
        






# 具体生成器
class QueryBuilder3(QueryBuilder):
    '''

# 定义提示模板字符串
template_str = """
Take a deep breath and work on this problem step-by-step

您是一个Python工程师, 我会提供给您一些已验证可用的代码(防止出现包版本过旧,或者环境不支持的情况),
在代码编写中,如果被验证代码块中存在相关内容,您应该尽可能的使用被验证的代码, 而非经验.
基于用户的需求和提供的已验证代码, 结合自己的经验,编写代码.
您编写的代码应该封装成函数或者类


已验证代码:
---
```python
{safe_code}
```
---

用户的诉求:
{prompt}

输出函数:
"""

# 创建PromptTemplate实例
qa_prompt = PromptTemplate(template=template_str)


class PythonQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate
    stream:bool

    def custom_query(self, query_str: str):
        # custom_query(query_str: str) -> STR_OR_RESPONSE_TYPE
        # acustom_query(query_str: str) -> STR_OR_RESPONSE_TYPE

        queries = query_str.split('&')
        nodes = []
        for query_str in queries:
            nodes += self.retriever.retrieve(query_str)
        # nodes = self.retriever.retrieve(query_str)
        print(query_str,'query_str')
        context_str = "\n\n".join([n.node.get_metadata_str() for n in nodes])
        if self.stream:
            response = self.llm.stream_complete(
                qa_prompt.format(safe_code=context_str, prompt=query_str)
            )

            def response_gen():
                i = [0]
                for r in response:
                    i.append(len(str(r)))
                    yield str(r)[i[-2]:]

            return StreamingResponse(response_gen=response_gen(),source_nodes=nodes)
        else:
            response = self.llm.complete(qa_prompt.format(safe_code=context_str, prompt=query_str))
    
            response_obj = self.response_synthesizer.synthesize(response.text, nodes)
            return Response(response=response.text,source_nodes=nodes) # TODO 增加metadata



    '''
   

    def get_query(self):
        # 例如：
            # instance = AnotherClass(param1=value1, param2=value2)
        
        
        retriever = index.as_retriever(similarity_top_k=similarity_top_k)
        query_engine = PythonQueryEngine(
                retriever=retriever,
                response_synthesizer=get_response_synthesizer(response_mode="compact"),
                llm=Settings.llm,
                qa_prompt=qa_prompt,
                stream = True,
            )

        return query_engine


