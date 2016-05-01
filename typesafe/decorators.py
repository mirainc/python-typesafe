# imports
from typesafe import Any, Class, Optional
from typesafe.errors import NotATypeError, InvalidTypeError, UnlabeledArgError
from types import NoneType

import inspect
from functools import wraps


# helper functions
def is_type(arg_type):
    if isinstance(arg_type, Optional):
        return is_type(arg_type._wrapped_type)
    elif isinstance(arg_type, list):
        return reduce(
            lambda all_types, next: all_types and is_type(next),
            arg_type,
            True
        )
    
    return inspect.isclass(arg_type)


def valid_type(arg_val, arg_type):
    if arg_type is Any:
        return True
    elif arg_type is Class:
        return inspect.isclass(arg_val)
    elif isinstance(arg_type, list):
        return reduce(
            lambda any_type, next: any_type or isinstance(arg_val, next),
            arg_type,
            False
        )
    elif isinstance(arg_type, Optional):
        return (
            valid_type(arg_val, arg_type._wrapped_type) or
            valid_type(arg_val, NoneType)
        )
    else:
        return isinstance(arg_val, arg_type)


# decorators
def args(**kwargs):
    intended_types = kwargs
    intended_types['self'] = Any
    
    for var_name, var_type in intended_types.items():
        if not is_type(var_type):
            raise NotATypeError(var_type)
    
    def decorator(function):
        inspected = inspect.getargspec(function)
        var_names = inspected.args
        
        for var_name in var_names:
            if var_name not in intended_types.keys():
                raise UnlabeledArgError(var_name)
        
        @wraps(function)
        def args_wrapper(*args, **kwargs):
            received_args = {}
            for index, arg_val in enumerate(args):
                
                if index >= len(var_names):
                    if inspected.varargs is not None:
                        # *args specified, skip trailing args
                        continue
                
                received_args[var_names[index]] = arg_val
            received_args.update(kwargs)
            
            for var_name, arg_val in received_args.items():
                
                if var_name not in intended_types:
                    if inspected.keywords is not None:
                        # **kwargs specified, skip trailing args
                        continue
                
                var_type = intended_types[var_name]
                if not valid_type(arg_val, var_type):
                    raise InvalidTypeError(var_name, arg_val, var_type)
            
            return function(*args, **kwargs)
        
        return args_wrapper
        
    return decorator


def returns(ret_type):
    if not is_type(ret_type):
        raise NotATypeError(ret_type)
    
    def decorator(function):
        if ret_type is Any:
            return function
        
        @wraps(function)
        def ret_wrapper(*args, **kwargs):
            ret_val = function(*args, **kwargs)
            if not valid_type(ret_val, ret_type):
                raise InvalidTypeError('returned value', ret_val, ret_type)
            return ret_val
        
        return ret_wrapper
    
    return decorator


def types(**kwargs):
    def decorator(function):
        ret_type = NoneType
        if 'returns' in kwargs:
            ret_type = kwargs['returns']
            del kwargs['returns']
        
        function = args(**kwargs)(function)
        function = returns(ret_type)(function)
        
        return function
    return decorator
