from .abc_ import QueryBuilder

# 指挥者
class Director:
    def __init__(self, builder:QueryBuilder):
        self.builder = builder

    def construct(self):
        self.builder.set_llm()
        self.builder.build_reader()
        self.builder.build_ingestion_pipeline()
        self.builder.build_storage_context()
        self.builder.build_index()
        self.builder.build_retriver()
        self.builder.build_query_pipeline()
        self.builder.build_tools()
        self.builder.build_kg_extractors()
        return self.builder.get_queryer()



# builderfactory


from enum import Enum
from typing import List, Any
from .builderlib import *


class BuilderType(Enum):
    ObsidianDateBuilder = 'ObsidianDateBuilder'
    ObsidianHabitBuilder = "ObsidianHabitBuilder"
    DeDaoJYRKBuilder = "DeDaoJYRKBuilder"
    TestGraphBuilder = "TestGraphBuilder"
    Test2GraphBuilder = "Test2GraphBuilder"
    simple = 'simple'
    # 添加更多选项

class BuilderFactory:
    def __new__(cls, type: BuilderType) -> Any:
        assert type.value in [i.value for i in BuilderType]
        instance = None

        if type.value == 'ObsidianDateBuilder':
            instance = ObsidianDateBuilder()

        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
            
        elif type.value == 'DeDaoJYRKBuilder':
            instance = DeDaoJYRKBuilder()
        elif type.value == 'TestGraphBuilder':
            instance = TestGraphBuilder()

        elif type.value == 'Test2GraphBuilder':
            instance = Test2GraphBuilder()
            
        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
        elif type.value == 'ObsidianHabitBuilder':
            instance = ObsidianHabitBuilder()
        else:
            raise Exception('Unknown type')

        return instance