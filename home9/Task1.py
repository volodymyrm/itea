import arrow


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class AbstractFactory(metaclass=Singleton):
    def create_monitor(self, model, diagonal):
        raise NotImplementedError()

    def create_system_unit(self, typ):
        raise NotImplementedError()

    def create_keyboard(self, typ):
        raise NotImplementedError()


class BaseComponent:
    def __init__(self):
        self.release_date = arrow.now().format('DD-MM-YYYY HH:mm:ss')


class Monitor(BaseComponent):
    def __init__(self, model, diagonal):
        super(Monitor, self).__init__()
        self.model = model
        self.diagonal = diagonal

    def __str__(self):
        return str(self.__dict__)


class Keyboard(BaseComponent):
    def __init__(self, typ):
        super(Keyboard, self).__init__()
        if typ in { "PC", "Bluetooth"}:
            self.typ = typ
        else:
            raise TypeError('Unsupported keyboard type')

    def __str__(self):
        return str(self.__dict__)


class SystemUnit(BaseComponent):
    def __init__(self, typ):
        super(SystemUnit, self).__init__()
        if typ in { "Mini tower", "Tower"}:
            self.typ = typ
        else:
            raise TypeError('Unsupported system unit type')
        self.typ = typ

    def __str__(self):
        return str(self.__dict__)


class Computer:
    def __init__(self):
        self.monitor = None
        self.keyboard = None
        self.system_unit = None

    def __str__(self):
        describe = 'Computer specification: \n'
        describe += 'Monitor: ' + str(self.__dict__.get('monitor')) + '\n'
        describe += 'Keyboard: ' + str(self.__dict__.get('keyboard')) + '\n'
        describe += 'System unit: ' + str(self.__dict__.get('system_unit')) + '\n'
        return describe


class Compus(AbstractFactory):
    def create_monitor(self, model, diagonal):
        monitor = Monitor(model, diagonal)
        monitor.vendor = self.__class__.__name__
        return monitor

    def create_keyboard(self, typ):
        keyboard = Keyboard(typ)
        keyboard.vendor = self.__class__.__name__
        return keyboard

    def create_system_unit(self, typ):
        system_unit = SystemUnit(typ)
        system_unit.vendor = self.__class__.__name__
        return system_unit

    def create_computer(self, **kwargs):
        computer = Computer()
        computer.monitor = self.create_monitor(kwargs.get('monitor_model', 'LCD monitor'), kwargs.get('monitor_diagonal', '21'))
        computer.keyboard = self.create_keyboard(kwargs.get('keyboard_type', 'PC'))
        computer.system_unit = self.create_system_unit(kwargs.get('unit_type', 'Tower'))
        return computer


factory = Compus()
print(factory.create_computer())
print(factory.create_computer(monitor_model='ELT', monitor_diagonal=23, keyboard_type='Bluetooth', unit_type='Mini tower'))