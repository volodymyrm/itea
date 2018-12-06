import re

class TypeValidator:
    """ Callable class. 
    :param value: stringified value
    :return value of appropriate type if its bool, int, float or string. Otherwise raises TypeError
    """
    def __init__(self, value):
        self.value = value

    @staticmethod
    def boolinator(value):
        if value.lower() == 'true':
            return 1, True
        elif value.lower() == 'false':
            return 1, False
        else:
            return 0, value

    @staticmethod
    def intator(value):
        try:
            return 1, int(value)
        except ValueError:
            return 0, value

    @staticmethod
    def floatator(value):
        try:
            return 1, float(value)
        except ValueError:
            return 0, value

    @staticmethod
    def stringator(value):
        if value.startswith('\'') and value.endswith('\''):
            return 1, value[1:-1]
        else:
            return 0, value

    def __call__(self):
        type_validators = [self.boolinator, self.intator, self.floatator, self.stringator]
        flag = 0
        for f in type_validators:
            if f(self.value)[0] == 1:
                self.result = f(self.value)[1]
                flag = 1
                return self.result
        if not flag:
            raise TypeError


def validate_name(name):
    """
    :param name: stringified variable name
    :return: raises NameError if name is not valid python variable lexeme
    """
    reg = re.compile('^[a-zA-Z_]+[a-zA-Z_0-9]*$')
    if not reg.match(name):
        raise NameError('Wrong variable name')


def validate_input(string):
    """
    Validate user input.
    :param string: String if format name=value, where name is variable name, value - its value
    :return: dictionary item {name: value} if input format is correct. Raise TypeError otherwise
    """
    try:
        inp = ''.join([x for x in list(string) if x != ' ']).split('=')
        validate_name(inp[0])
        return {inp[0]: TypeValidator(inp[1])()}
    except:
        raise TypeError('Wrong input format')


def output(self):
    """
    
    :param self: 
    :return: 
    """
    describe = 'Class <{}>:\n'.format(self.__class__.__name__)
    params='\n'.join(['{key} = {value}'.format(key=k, value=v) for k,v in self.__class__.__dict__.items() if not k.startswith('__')])
    return describe + params

def main():
    classname = input('Classname = ')
    params = {}
    while True:
        a = input('Set up class items ')
        if a != '':
            try:
                params.update(validate_input(a))
            except Exception:
                print('Input class properties in name=value format. Name is valid Python variable lexeme. '
                      'value could be bool, int, float or string. String value should be in single brackets')
        else:
            break

    params.update({'__str__': output})
    Myclass = type(classname, (), params)
    a = Myclass()
    print(a)

if __name__== "__main__":
    main()
