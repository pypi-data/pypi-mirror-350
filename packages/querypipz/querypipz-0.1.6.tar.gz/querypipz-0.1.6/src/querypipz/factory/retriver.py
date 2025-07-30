

from enum import Enum
from typing import List, Any

from enum import Enum
from typing import List, Any
from llama_index.core.readers.base import BaseReader
from typing import List, Dict,Optional
from llama_index.core import Document
import yaml



from enum import Enum
from typing import List, Any

class RetriverType(Enum):
    Simple = 'Simple'
    Simple2 = 'Simple2'
    # 添加更多选项

class Retriver:
    def __new__(cls, type: RetriverType) -> Any:
        assert type.value in [i.value for i in RetriverType]
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
    
def build_retriver(self):
    self.query.retriver = VectorIndexRetriever