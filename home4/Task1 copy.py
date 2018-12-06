import re

class Context:

    class __ContextIterator:
        def __init__(self, context_instance):
            self.context_instance_iter = context_instance.items().__iter__()

        def __next__(self):
            return dict((next(self.context_instance_iter),))

    context = {}

    def __init__(self, **kvargs):
        self.context.update(kvargs)

    def __str__(self):
        describe = "Class ("
        for keys, values in self.context.items():
            describe += '{key} = {value}, '.format(key=keys, value=values)
        describe = describe[:-2] + ')'
        return describe

    def __setattr__(self, key, value):
        self.validate_name(key)
        self.context.update({key:value})

    def __getattr__(self, key):
        return self.context[key]

    def __len__(self):
        return len(self.context)

    def __iter__(self):
        return self.__ContextIterator(self.context)

    @staticmethod
    def validate_name(name):
        reg = re.compile('^[a-zA-Z_]+[a-zA-Z_0-9]*$')
        if not reg.match(name):
            raise NameError('Wrong variable name')


obj = Context(a=10, b=3, c='abc')

iterator = iter(obj)
# print (next(iterator))
# print (next(iterator))



for item in obj:
    print(item)


# print(obj.context)
# print(obj)
# print(len(obj))