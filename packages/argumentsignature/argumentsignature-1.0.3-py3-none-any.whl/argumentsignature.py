from typing import Type, Generic, TypeVar

__version__ = '1.0.3'

TCallable = TypeVar("TCallable")

class ArgumentType:
    def __init__(self, name:str):
        self.name = name
          
    def __str__(self):
        return self.name

EMPTY = Ellipsis
ARG = ArgumentType(name='ARG')
ARGS = ArgumentType(name='ARGS')
KWARGS = ArgumentType(name='KWARGS')
RETURN = ArgumentType(name='RETURN')

class Argument(Generic[TCallable]):
    def __init__(self, name:str, type:Type[TCallable], default:TCallable=EMPTY, argtype:ArgumentType=ARG):
        self.name = name
        self.type = type
        self.default = default
        self.argtype = argtype
    
    def to_argument_value(self, value:TCallable) -> 'ArgumentValue[TCallable]':
        return ArgumentValue(
            name = self.name,
            type = self.type,
            value = value,
            default = self.default,
            argtype = self.argtype       
        )
    
    def __str__(self):
        local_dict = self.__dict__.copy()
        if isinstance(self.default, str):
            local_dict['default'] = "'{}'".format(self.default)
        items = list(map(lambda i: i[0]+': '+str(i[1]), local_dict.items()))
        return "{}({})".format(self.__class__.__name__, ', '.join(items))


class ArgumentValue(Argument[TCallable], Generic[TCallable]):
    def __init__(self, name:str, type:Type[TCallable], value:TCallable, default:TCallable=EMPTY, argtype:ArgumentType=ARG):
        super().__init__(name=name, type=type, default=default, argtype=argtype)
        self.value = value

    def to_argument(self) -> Argument[TCallable]:
        return Argument(
            name = self.name,
            type = self.type,
            default = self.default,
            argtype = self.argtype       
        )
    
    def __str__(self):
        local_dict = self.__dict__.copy()
        if isinstance(self.default, str):
            local_dict['default'] = "'{}'".format(self.default)
        if isinstance(self.value, str):
            local_dict['value'] = "'{}'".format(self.value)
        items = list(map(lambda i: i[0]+': '+str(i[1]), local_dict.items()))
        return "{}({})".format(self.__class__.__name__, ', '.join(items))

def is_default_argument(argument:Argument):
    return argument.argtype is ARG and argument.default is not EMPTY

__all__ = [
    'ArgumentType',
    'Argument',
    'ArgumentValue',
    'EMPTY',
    'ARG',
    'ARGS',
    'KWARGS',
    'RETURN',
    'is_default_argument'
]
