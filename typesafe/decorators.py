# imports
from typesafe import Any, Class
from typesafe.errors import NotATypeError, InvalidTypeError, UnlabeledArgError
from types import NoneType
import inspect


# helper functions
def valid_type(arg_val, arg_type):
    if arg_type is Any:
        return True
    elif arg_type is Class:
        return inspect.isclass(arg_val)
    else:
        return isinstance(arg_val, arg_type)


# decorators
def args(**kwargs):
    intended_types = kwargs
    intended_types['self'] = Any
    
    for var_name, var_type in intended_types.items():
        if not inspect.isclass(var_type):
            raise NotATypeError(var_type)
    
    def decorator(function):
        var_names = inspect.getargspec(function).args
        for var_name in var_names:
            if var_name not in intended_types.keys():
                raise UnlabeledArgError(var_name)
        
        def args_wrapper(*args, **kwargs):
            received_args = {}
            for index, arg_val in enumerate(args):
                received_args[var_names[index]] = arg_val
            received_args.update(kwargs)
            
            for var_name, arg_val in received_args.items():
                var_type = intended_types[var_name]
                if not valid_type(arg_val, var_type):
                    raise InvalidTypeError(var_name, arg_val, var_type)
            
            return function(*args, **kwargs)
        
        return args_wrapper
        
    return decorator


def returns(ret_type):
    if not inspect.isclass(ret_type):
        raise NotATypeError(ret_type)
    
    def decorator(function):
        if ret_type is Any:
            return function
        
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
