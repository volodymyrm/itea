from abc import ABCMeta, abstractmethod
import re


class ValidationError(Exception):
    """
    Self defined exception, used in RealComplex class.
    Raises when trying to add neither complex nor real type attribute.
    """
    pass

class NumberBaseContext:
    """
    Abstract interface class
    """
    __metaclass__=ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        """ Self defined constructor with specific validation"""

    @abstractmethod
    def __setattr__(self, key, value):
        """Self defined setattr with specific validation"""

    @staticmethod
    @abstractmethod
    def validate_type(name):
        """Validation of context values"""


class Context:
    """
    Stores context of variables and their values as dictionary
    """

    def __init__(self, **kwargs):
        """
        Class constructor
        :param kwargs: values that will be added to class context on object
         initialization
        """
        self.__dict__['context'] = {}
        for key, value in kwargs.items():
            reg = re.compile('^[a-zA-Z_]+[a-zA-Z_0-9]*$')
            if not reg.match(key):
                raise NameError('Wrong variable name')
            self.validate_name(key)
        self.context.update(kwargs)

    def __str__(self):
        """
        Prints object context
        :return: string like: Class (a = 10, b = 'a')
        """
        describe = "Class ("
        for keys, values in self.context.items():
            describe += '{key} = {value}, '.format(key=keys, value=values)
        describe = describe[:-2] + ')' if self.context.items() else\
            describe + (')')
        return describe

    def __setattr__(self, key, value):
        """
        Add item to class context as setting class attribute
        :param key: variable name
        :param value: variable value
        :return: None
        """
        reg = re.compile('^[a-zA-Z_]+[a-zA-Z_0-9]*$')
        if not reg.match(key):
            raise NameError('Wrong variable name')
        self.context.update({key:value})

    def __getattr__(self, key):
        """
        Getting context attribute value as class attribute value
        :param key: variable name from context
        :return: variable value
        """
        return self.context[key]

    def __len__(self):
        """
        Counts number of context values
        :return: number of context values
        """
        return len(self.context)

    def __iter__(self):
        """
        Makes class iterable
        :return: next item from context
        """
        for key, value in self.context.items():
            yield {key: value}

    @staticmethod
    def validate_name(name):
        """
        Context item name validator stub
        :return: True
        """


class RealContext(Context):
    """
    Context child with strong data validation. Accept int and float values only
    """
    def __init__(self, **kwargs):
        """
        Class constructor. Inherits from parent and applies self validation
        """
        Context.__init__(self, **kwargs)
        for key, value in self.context.items():
            self.validate_type(value)
        self.context.update(kwargs)

    def __setattr__(self, key, value):
        """
        Inherits __setattr__ from parent and applies self validation
        """
        Context.__setattr__(self, key, value)
        self.validate_type(value)
        self.context.update({key:value})

    @staticmethod
    def validate_type(name):
        """
        Context item type validator
        :param name: value for validation
        :return: raises TypeError if value neither float nor int
        """
        print('RealContext validation call')
        if not (isinstance(name, int) or isinstance(name, float)):
            raise TypeError ('Wrong variable type (Neither int nor float)')


class ComplexContext(Context):
    """
    Context child with strong data validation. Accept real values only
    """
    def __init__(self, **kwargs):
        """
        Class constructor. Inherits from parent and applies self validation
        """
        Context.__init__(self, **kwargs)
        for key, value in self.context.items():
            self.validate_type(value)
        self.context.update(kwargs)

    def __setattr__(self, key, value):
        """
        Inherits __setattr__ from parent and applies self validation
        """
        Context.__setattr__(self, key, value)
        self.validate_type(value)
        self.context.update({key: value})

    @staticmethod
    def validate_type(name):
        """
        Context item type validator
        :param name: value for validation
        :return: raises TypeError if value in not complex
        """
        print('ComplexContext validation call')
        if not isinstance(name, complex):
            raise TypeError('Wrong variable type (Not Complex)')


class NumberContext(NumberBaseContext, RealContext, ComplexContext):
    """
    Context child with strong data validation. Accept real values only
    """
    def __init__(self, **kwargs):
        """
        Class constructor. Inherits from parent and applies self validation
        """
        Context.__init__(self, **kwargs)
        for key, value in self.context.items():
            self.validate_type(value)
        self.context.update(kwargs)

    def __setattr__(self, key, value):
        """
        Inherits __setattr__ from parent and applies self validation
        """
        Context.__setattr__(self, key, value)
        self.validate_type(value)
        self.context.update({key: value})

    @staticmethod
    def validate_type(value):
        """
        Context item type validator
        :param value: value for validation
        :return: raises ValidationError if value is other then 
                int, float, complex
        """
        print('NumberContext validation call')
        err_count = 0
        try:
            RealContext.validate_type(value)
        except TypeError:
            err_count += 1
        try:
            ComplexContext.validate_type(value)
        except TypeError:
            err_count += 1
        if err_count == 2:
            raise ValidationError('Variable type neither real nor complex')


# with Context(x=1, v=2) as c:
#     print (x, v)
#
# print(x,y)