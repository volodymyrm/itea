from home4 import Context

class ContextManager(Context):

    def __enter__(self, **kwargs):
        self.context.update(**kwargs)
        for k, v in self.context.items():
            globals()[k] = v

    def __exit__(self, exc_type, exc_val, exc_tb):
        for k, v in self.context.items():
            del globals()[k]



with ContextManager(x=1, v=2) as c:
    print (x, v)

# print(x,y) - leads to error