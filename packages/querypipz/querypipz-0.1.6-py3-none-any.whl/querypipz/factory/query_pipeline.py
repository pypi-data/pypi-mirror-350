from enum import Enum
from typing import List, Any
from llama_index.core import SimpleDirectoryReader


class QueryType(Enum):
    Simple = 'Simple'
    Simple2 = 'Simple2'
    # 添加更多选项

class Query:
    def __new__(cls, type: QueryType) -> Any:
        assert type.value in [i.value for i in QueryType]
        instance = None

        if type.value == 'Simple':

            # instance = SomeClass(param1=value1, param2=value2)
            pass

        elif type.value == 'Simple2':

            # instance = AnotherClass(param1=value1, param2=value2)
            pass


        else:
            raise Exception('Unknown type')

        return instance


def build_query_pipeline(self):
    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=self.query.retriver,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )
    self.query_pipeline = query_engine
