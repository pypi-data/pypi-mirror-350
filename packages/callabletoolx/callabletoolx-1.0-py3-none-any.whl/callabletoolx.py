from typing import Any, Dict, List, TypeVar, Callable, Optional, Any, overload
from types import CodeType
from argumentsignature import (
    Argument, ArgumentValue, ARG, ARGS, KWARGS, RETURN, is_default_argument
)

__version__ = '1.0'

TCallable = TypeVar("TCallable", bound=Callable)

@overload
def get_code(callable:TCallable) -> CodeType: ...
@overload
def get_code(code:CodeType) -> CodeType: ...
def get_code(call_or_code) -> CodeType:
    return call_or_code if isinstance(call_or_code, CodeType) else call_or_code.__code__



@overload
def has_args_params(callable:TCallable) -> bool: ...
@overload
def has_args_params(code:CodeType) -> bool: ...
def has_args_params(call_or_code) -> bool:
    return bool(get_code(call_or_code).co_flags  & 0x04)

@overload
def has_kwargs_params(callable:TCallable) -> bool: ...
@overload
def has_kwargs_params(code:CodeType) -> bool: ...
def has_kwargs_params(call_or_code) -> bool:
    return bool(get_code(call_or_code).co_flags  & 0x08)


@overload
def get_argument_length(callable:TCallable) -> bool: ...
@overload
def get_argument_length(code:CodeType) -> bool: ...
def get_argument_length(call_or_code) -> int:
    code = get_code(call_or_code)
    return code.co_argcount + code.co_kwonlyargcount + has_args_params(code) + has_kwargs_params(code)

def get_arguments(callable:TCallable) -> List[Argument]:
    annotations = callable.__annotations__
    code = callable.__code__
    varnames = code.co_varnames
    defaults = callable.__kwdefaults__ or {}
    arg_names = varnames[:code.co_argcount]
    default_names = list(defaults.keys())
    total_arg_count = code.co_argcount + len(defaults)

    argumanList:List[Argument] = []
    for arg_name in arg_names:
        argumanList.append(Argument(name=arg_name, type=annotations.get(arg_name, Any), argtype=ARG))
    if has_args_params(code):
        arg_name = varnames[total_arg_count]
        argumanList.append(Argument(name=arg_name, type=annotations.get(arg_name, Any), argtype=ARGS))
    for arg_name in default_names:
        argumanList.append(Argument(
            name=arg_name, type=annotations.get(arg_name, Any), default=defaults[arg_name], argtype=ARG
        ))
    if has_kwargs_params(code):
        arg_name = varnames[total_arg_count+1 if has_args_params(code) else total_arg_count]
        argumanList.append(Argument(name=arg_name, type=annotations.get(arg_name, Any), argtype=KWARGS))
    return argumanList

def get_return_argument(callable:TCallable) -> Optional[Argument]:
    annotations = callable.__annotations__
    argument = None
    if 'return' in annotations:
        if annotations['return'] is not None:
            argument = Argument(name = 'return', type = annotations['return'], argtype = RETURN)
    return argument

def get_argument_values(arguments:List[Argument], args:List[Any], kwargs:Dict[str,Any]) -> List[ArgumentValue]:
    argument_values = []
    kwargs = kwargs.copy()
    is_args = False
    for index, argument in enumerate(arguments):
        if argument.argtype == ARG:
            if not is_default_argument(argument):
                argument_values.append(argument.to_argument_value(args[index]))
            else:
                if argument.name in kwargs:
                    value = kwargs[argument.name]
                    kwargs.pop(argument.name)
                else:
                    value = argument.default if is_args else args[index]
                argument_values.append(argument.to_argument_value(value))
        elif argument.argtype == ARGS:
            argument_values.append(argument.to_argument_value(args[index:]))
            is_args = True
        elif argument.argtype == KWARGS:
            argument_values.append(argument.to_argument_value(kwargs))
    return argument_values

__all__ = [
    'get_code',
    'has_args_params',
    'has_kwargs_params',
    'get_arguments',
    'get_argument_length',
    'get_return_argument',
    'get_argument_values'
]
