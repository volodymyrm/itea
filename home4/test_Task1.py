from Task1 import *

class TestClass(object):
    """
    Testing class for homework1. To run all tests with pytest,
    run the following command in current path:
    $ pytest
    """
    def test_context_init(self):
        obj = Context(a=1, b=1.0, c=1+2j, d='abc')
        assert obj.a == 1
        assert obj.b == 1.0
        assert obj.c == 1+2j
        assert obj.d == 'abc'

    def test_context_setattr(self):
        obj = Context()
        obj.a = 100
        assert obj.a == 100

    def test_context_len(self):
        obj = Context(a=1, b=1.0, c=1 + 2j, d='abc')
        assert len(obj) == 4

    def test_context_print(self):
        obj1 = Context(e=1)
        assert str(obj1.__str__()) == 'Class (e = 1)'

    def test_context_iter(self):
        obj = Context(a=1, b=1.0, c=2, d='abc')
        iterator = iter(obj)
        assert next(iterator) == {'a': 1}
        assert next(iterator) == {'b': 1.0}
        assert next(iterator) == {'c': 2}
        assert next(iterator) == {'d': 'abc'}
        try:
            next(iterator)
        except StopIteration:
            assert True

    def test_real_context_validate_type(self):
        obj = RealContext(a=1, b=1.0)
        assert obj.a == 1
        assert obj.b == 1.0
        try:
            obj.c = 'abc'
        except TypeError:
            assert True

    def test_complex_context_validate_type(self):
        obj = ComplexContext(a=1+2j)
        assert obj.a == 1 + 2j
        try:
            obj.b = 'abc'
        except TypeError:
            assert True

    def test_NumberContext_validate_type(self):
        obj = NumberContext(a=1, b=1.0, c=1+2j)
        try:
            obj.d='abc'
        except ValidationError:
            assert True


