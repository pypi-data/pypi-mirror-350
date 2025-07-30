

from llama_index.core.graph_store.types import (
    EntityNode,
    Relation,
    KG_NODES_KEY,
    KG_RELATIONS_KEY,
)
from llama_index.core.schema import BaseNode, TransformComponent

from enum import Enum
from typing import Any
from llama_index.core.indices.property_graph.transformations import ImplicitPathExtractor,SchemaLLMPathExtractor,SimpleLLMPathExtractor, DynamicLLMPathExtractor




class MyGraphExtractor(TransformComponent):
    # the init is optional
    # def __init__(self, ...):
    #     ...

    def __call__(
        self, llama_nodes: list[BaseNode], **kwargs
    ) -> list[BaseNode]:
        for llama_node in llama_nodes:
            # be sure to not overwrite existing entities/relations

            existing_nodes = llama_node.metadata.pop(KG_NODES_KEY, [])
            existing_relations = llama_node.metadata.pop(KG_RELATIONS_KEY, [])

            existing_nodes.append(
                EntityNode(
                    name="llama", label="ANIMAL", properties={"key": "val"}
                )
            )
            existing_nodes.append(
                EntityNode(
                    name="index", label="THING", properties={"key": "val"}
                )
            )

            existing_relations.append(
                Relation(
                    label="HAS",
                    source_id="llama",
                    target_id="index",
                    properties={},
                )
            )

            # add back to the metadata

            llama_node.metadata[KG_NODES_KEY] = existing_nodes
            llama_node.metadata[KG_RELATIONS_KEY] = existing_relations

        return llama_nodes

    # optional async method
    # async def acall(self, llama_nodes: list[BaseNode], **kwargs) -> list[BaseNode]:
    #    ...



class GraphExtractorType(Enum):
    MyGraphExtractor = 'MyGraphExtractor'
    DynamicLLMPathExtractor = "DynamicLLMPathExtractor"
    DynamicLLMPathExtractor2 = "DynamicLLMPathExtractor2"
    SchemaLLMPathExtractor = "SchemaLLMPathExtractor"
    SimpleLLMPathExtractor = "SimpleLLMPathExtractor"
    ImplicitPathExtractor = "ImplicitPathExtractor"
    # Add more options as needed


class GraphExtractor:
    def __new__(cls, type: GraphExtractorType) -> Any:
        assert type.value in [i.value for i in GraphExtractorType]
        instance = None

        if type.value == 'MyGraphExtractor':
            instance = MyGraphExtractor()

        elif type.value == 'MyGraphExtractor':
            instance = MyGraphExtractor()
        elif type.value == 'MyGraphExtractor':
            instance = MyGraphExtractor()

        elif type.value == 'SimpleLLMPathExtractor':
            instance = SimpleLLMPathExtractor()
        elif type.value == 'ImplicitPathExtractor':
            instance = ImplicitPathExtractor()
            
        elif type.value == 'DynamicLLMPathExtractor':
            instance = DynamicLLMPathExtractor(
                                                max_triplets_per_chunk=20,
                                                num_workers=4,
                                                allowed_entity_types=["POLITICIAN", "POLITICAL_PARTY"],
                                                allowed_relation_types=["PRESIDENT_OF", "MEMBER_OF"],
                                                allowed_relation_props=["description"],
                                                allowed_entity_props=["description"],
                                            )
            
        elif type.value == 'DynamicLLMPathExtractor2':
            instance  = DynamicLLMPathExtractor(
                                                max_triplets_per_chunk=20,
                                                num_workers=4,
                                                # Let the LLM infer entities and their labels (types) on the fly
                                                allowed_entity_types=None,
                                                # Let the LLM infer relationships on the fly
                                                allowed_relation_types=None,
                                                # LLM will generate any entity properties, set `None` to skip property generation (will be faster without)
                                                allowed_relation_props=[],
                                                # LLM will generate any relation properties, set `None` to skip property generation (will be faster without)
                                                allowed_entity_props=[],
                                            )
        elif type.value == 'SchemaLLMPathExtractor':
            instance = SchemaLLMPathExtractor(
                                            llm = llm,
                                            max_triplets_per_chunk=20,
                                            strict=False,  # Set to False to showcase why it's not going to be the same as DynamicLLMPathExtractor
                                            possible_entities=None,  # USE DEFAULT ENTITIES (PERSON, ORGANIZATION... etc)
                                            possible_relations=None,  # USE DEFAULT RELATIONSHIPS
                                            possible_relation_props=[
                                                "extra_description"
                                            ],  # Set to `None` to skip property generation
                                            possible_entity_props=[
                                                "extra_description"
                                            ],  # Set to `None` to skip property generation
                                            num_workers=4,
                                            )
            
        else:
            raise Exception('Unknown type')

        return instance









