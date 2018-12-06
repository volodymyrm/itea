class LimitExceedError(StandardError):
    """
    Self defined exception, used in Stack class.
    Raises when trying to push item when stack limit exceeded.
    """
    pass


class EmptyStackError(StandardError):
    """
    Self defined exception, used in Stack class.
    Raises when trying to pull item from empty stack.
    """
    pass


class Stack:
    """
    Class <Stack>
    Uses for storing items in FILO queue.
    """
    def __init__(self, limit=None, data_type=object):
        """
        Class constructor
        :param limit: number of items that can be stored.
        :param data_type: acceptable data type of items that can be stored.
        """
        self.__items = []
        self.limit = limit
        self.data_type = data_type

    def __str__(self):
        """
        :return: string in format "Stack<type of data>".
        """
        return 'Stack<{}>'.format(str(self.type)[7:-2])

    def _push(self, item):
        """
        Check if pushing to stack possible regarding its data type and limit.
        :param item: item to be pushed.
        :raise: LimitExceedError: if stack limit exceeded.
        :raise: TypeError: if trying to push element of other type.
        """
        if self.count() >= self.limit:
            raise LimitExceedError

        if not isinstance(item, self.data_type):
            raise TypeError

    def push(self, item):
        """
        Insert item to stack.
        :param item: item to be pushed.
        """
        self._push(item)
        self.__items.insert(0, item)

    def pull(self):
        """
        Extract top item from stack.
        :return: top item of stack. 
        :raise: EmptyStackError: if pulling from empty stack.
        """
        try:
            return self.__items.pop(0)
        except IndexError:
            raise EmptyStackError

    def count(self):
        """
        Counting number of items in stack.
        :return: number of stack items.
        """
        return len(self.__items)

    def clear(self):
        """
        Clear the stack
        """
        self.__items = []

    @property
    def type(self):
        """
        Defining stack data type.
        :return: data_type: stack data type.
        """
        return self.data_type

