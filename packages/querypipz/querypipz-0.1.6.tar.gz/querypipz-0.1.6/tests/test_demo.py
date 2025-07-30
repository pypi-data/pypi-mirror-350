import pytest

from querypipz.director import Director
from querypipz.builderlib import ObsidianDateBuilder


@pytest.fixture
def queryer():
    builder = ObsidianDateBuilder()
    director = Director(builder)
    query = director.construct()
    yield query

def test_query_q2(queryer):
    queryer.build()


def test_query_q(queryer):
    print(queryer.retrieve('hello'))

def test_query_q3(queryer):
    print(queryer.query('hello'))



#做到另一个服务中?
# chat
# workflow





