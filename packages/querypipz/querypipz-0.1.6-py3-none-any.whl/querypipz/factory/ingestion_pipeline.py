
from enum import Enum
from typing import List, Any
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import TokenTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BIANXIE_API_KEY")
api_base = os.getenv("BIANXIE_BASE")
Settings.embed_model = OpenAIEmbedding(api_key=api_key,api_base =api_base)

class SplitterType(Enum):
    Simple = 'Simple'
    Simple2 = 'Simple2'
    TokenTextSplitter = "TokenTextSplitter"
    # 添加更多选项

class Splitter:
    def __new__(cls, type: SplitterType) -> Any:
        assert type.value in [i.value for i in SplitterType]
        instance = None

        if type.value == 'Simple':
            instance = SentenceSplitter(chunk_size=4096)

        elif type.value == 'Simple2':
            instance = SentenceSplitter(chunk_size=512, chunk_overlap=10)

        elif type.value == 'TokenTextSplitter':
            instance = TokenTextSplitter()

            
        else:
            raise Exception('Unknown type')

        return instance



#################


from llama_index.core.readers.base import BaseReader
from typing import List, Dict,Optional
from llama_index.core import Document
import yaml
from llmada import BianXieAdapter
from llmada import GoogleAdapter

import re

from llama_index.core.schema import TransformComponent



def extract_n_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```原文摘抄([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches[0]




class DeDaoCleaner(TransformComponent):
    def __call__(self, nodes, **kwargs):
        # print(nodes,'nodes')
        prompt = Templates(TemplateType.DedaoExtract)
        bx = GoogleAdapter("AIzaSyBH4ut1plgB95fEiBlBXq1S-VrdYY5xPU4")
        for node in nodes:
            result = bx.product(prompt.format(text = node.text))
            node.set_content(self._extract_n_code(result))
        return nodes

    def _extract_n_code(self,text: str)->str:
        """从文本中提取python代码

        Args:
            text (str): 输入的文本。

        Returns:
            str: 提取出的python文本
        """
        pattern = r'```原文摘抄([\s\S]*?)```'
        matches = re.findall(pattern, text)
        return matches[0]



class CleanerType(Enum):
    DeDaoCleaner = 'DeDaoCleaner'
    Simple2 = 'Simple2'
    # 添加更多选项

class Cleaner:
    def __new__(cls, type: CleanerType) -> Any:
        assert type.value in [i.value for i in CleanerType]
        instance = None

        if type.value == 'DeDaoCleaner':
            instance = SentenceSplitter(chunk_size=4096)

        elif type.value == 'Simple2':
            instance = SentenceSplitter(chunk_size=512, chunk_overlap=10)
        else:
            raise Exception('Unknown type')

        return instance



######################



from llama_index.embeddings.openai import OpenAIEmbedding

class EmbeddingType(Enum):
    OpenAIEmbedding = 'OpenAIEmbedding'
    Simple2 = 'Simple2'
    # 添加更多选项

class Embedding:
    def __new__(cls, type: EmbeddingType) -> Any:
        assert type.value in [i.value for i in EmbeddingType]
        instance = None

        if type.value == 'OpenAIEmbedding':
            instance = OpenAIEmbedding()

        elif type.value == 'Simple2':
            instance = SentenceSplitter(chunk_size=512, chunk_overlap=10)
        else:
            raise Exception('Unknown type')

        return instance

