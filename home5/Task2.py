class ConstAttributeError(Exception):
    """
    Self defined exception. Raises when trying to change class attribute value
    """
    pass


class Const(type):
    """
    Metaclass that prevents changing classes attributes values
    """
    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            raise ConstAttributeError("Attribute can't be changed")
        else:
            super(Const, self).__setattr__(key, value)
