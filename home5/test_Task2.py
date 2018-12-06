from Task2 import *

class A(metaclass=Const):
    x = 1

class TestClass:
    def test_set_new_attr(self):
        A.y = 2
        assert A.y == 2

    def test_change_attr(self):
        try:
            A.x = 1
        except Exception as e:
            assert isinstance(e, ConstAttributeError)

    def test_set_obj_attr(self):
        a = A()
        a.x = 100
        assert a.x == 100

    def test_change_obj_attr(self):
        a = A()
        a.x = 100
        a.x = 200
        assert a.x == 200
