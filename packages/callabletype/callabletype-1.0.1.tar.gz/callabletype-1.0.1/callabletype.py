from typing import List, Callable, TypeVar, Optional
import types

__version__ = '1.0.1'

TCallable = TypeVar('TCallable', bound=Callable)

class CallableType:
    def __init__(
        self, name:str, allowed_types:Optional[List['CallableType']]=None, 
        check_func:Callable[[TCallable],bool]=lambda t:True
    ):
        self.name = name
        self.allowed_types = allowed_types if allowed_types is not None else []
        self.check_func = check_func

    def __repr__(self) -> str:
        return "{}({})".format(self.name,",".join(map(lambda t: t.name, self.allowed_types)))
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, callable_type:'CallableType') -> bool:
        return self.__contains__(callable_type)
    
    def __ne__(self, callable_type:'CallableType'):
        return not self.__contains__(callable_type)

    def __contains__(self, callable_type:'CallableType') -> bool:
        return callable_type in self.allowed_types or callable_type is self

def get_callable_type(obj:TCallable) -> Optional[CallableType]:
    if CALLABLE.check_func(obj):
        for callable_type in CALLABLE.allowed_types:
            if callable_type.check_func(obj):
                return callable_type
        return CALLABLE
    return None

def is_staticmethod(obj:TCallable) -> bool:
    if not is_function(obj):
        return False
    return not (is_selfmethod(obj) or is_classmethod(obj))

STATICMETHOD = CallableType(
    name = 'SELFMETHOD',
    check_func = is_staticmethod
)

def is_instanceselfmethod(obj:TCallable) -> bool:
    return hasattr(obj, '__self__') and is_selfmethod(obj)        

INSTANCESELFMETHOD = CallableType(
    name = 'INSTANCESELFMETHOD',
    check_func = is_instanceselfmethod
)

def is_selfmethod(obj:TCallable) -> bool:
    if not is_function(obj):
        return False
    args = obj.__code__.co_varnames
    return args[0] == 'self' if args else False

SELFMETHOD = CallableType(
    name = 'SELFMETHOD',
    allowed_types=[INSTANCESELFMETHOD],
    check_func = is_selfmethod
)

def is_classmethod(obj:TCallable) -> bool:
    if not is_function(obj):
        return False
    args = obj.__code__.co_varnames
    return args[0] == 'cls' if args else False

CLASSMETHOD = CallableType(
    name = 'CLASSMETHOD',
    check_func = is_classmethod
)

def is_method(obj:TCallable) -> bool:
    if not is_function(obj):
        return False
    return isinstance(obj, types.MethodType) or is_selfmethod(obj) or is_classmethod(obj)

METHOD = CallableType(
    name = 'METHOD', 
    allowed_types = [INSTANCESELFMETHOD, SELFMETHOD, CLASSMETHOD, STATICMETHOD],
    check_func = is_method
)

def is_function(obj:TCallable) -> bool:
    return isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType)

FUNCTION = CallableType(
    name ='FUNCTION',
    allowed_types = [
        INSTANCESELFMETHOD,
        SELFMETHOD, 
        CLASSMETHOD,
        STATICMETHOD,
        METHOD,
    ],
    check_func= is_function
)

def is_class(obj:TCallable) -> bool:
    return isinstance(obj, type)

CLASS = CallableType(
    name='CLASS',
    check_func=is_class  
)

def is_callable(obj:TCallable) -> bool:
    return callable(obj)

CALLABLE = CallableType(
    name='CALLABLE', 
    allowed_types=[
        CLASS,
        INSTANCESELFMETHOD,
        SELFMETHOD,
        CLASSMETHOD,
        STATICMETHOD,
        METHOD,
        FUNCTION,
    ],
    check_func=is_callable,
)



__all__ = [
    'CallableType',
    'get_callable_type',
    'CALLABLE',
    'is_callable',
    'CLASS',
    'is_class',
    'FUNCTION',
    'is_function',
    'METHOD',
    'is_method',
    'CLASSMETHOD',
    'is_classmethod',
    'SELFMETHOD',
    'is_selfmethod',
    'STATICMETHOD',
    'is_staticmethod',
    "INSTANCESELFMETHOD",
    "is_instanceselfmethod"
]
