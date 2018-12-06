from home1 import Stack
from home1 import LimitExceedError
from home1 import EmptyStackError
import pytest

class TestClass(object):
    """
    Testing class for homework1. To run all tests with pytest,
    run the following command in current path:
    $ pytest
    """
    def test_init_empty(self):
        s = Stack()
        assert s.limit is None
        assert s.type is object

    def test_init_set(self):
        s = Stack(data_type=float, limit=10)
        assert s.limit == 10
        assert s.type is float

    def test__push_limit_error(self):
        s = Stack(data_type=int, limit=0)
        with pytest.raises(LimitExceedError):
            s._push(2)

    def test__push_type_error(self):
        s = Stack(data_type=int, limit=2)
        with pytest.raises(TypeError):
            s._push(2.1)

    def test_push_ok(self):
        s = Stack(data_type=str, limit=10)
        s.push('Vova')
        assert s.pull() == 'Vova'

    def test_pull_ok(self):
        s = Stack(data_type=int, limit=5)
        s.push(1)
        s.push(2)
        assert s.pull() == 2

    def test_pull_error(self):
        s = Stack(data_type=int, limit=10)
        s.push(1)
        s.pull()
        with pytest.raises(EmptyStackError):
            s.pull()

    def test_count(self):
        s = Stack(data_type=str, limit=5)
        s.push('a')
        s.push('b')
        s.push('c')
        assert s.count() == 3

    def test_clear(self):
        s = Stack(data_type=str, limit=5)
        s.push('a')
        s.push('b')
        s.push('c')
        s.clear()
        assert s.count() == 0

    def test_type(self):
        s = Stack(data_type=bool)
        assert s.type is bool

    def test_str(self):
        s = Stack()
        assert s.__str__() == 'Stack<object>'
