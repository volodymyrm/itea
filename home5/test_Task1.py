from Task1 import *

class TestClass(object):

    def test_validate_bool(self):
        a = 'tRue'
        assert TypeValidator(a)() == True
        assert isinstance(TypeValidator(a)(), bool)

    def test_validate_int(self):
        a = '100'
        assert TypeValidator(a)() == 100
        assert isinstance(TypeValidator(a)(), int)

    def test_validate_float(self):
        a = '2.1'
        assert TypeValidator(a)() == 2.1
        assert isinstance(TypeValidator(a)(), float)

    def test_validate_string(self):
        a = '\'abc\''
        assert TypeValidator(a)() == 'abc'
        assert isinstance(TypeValidator(a)(), str)

    def test_valid_name_pos(self):
        name = 'a1'
        try:
            validate_name(name)
            assert True
        except NameError:
            assert False

    def test_valid_name_neg(self):
        name = '1a'
        try:
            validate_name(name)
            assert False
        except Exception:
            assert True

    def test_validate_input(self):
        string = 'a   = 10'
        assert validate_input(string) == {'a':10}