# imports
from typesafe import Any
from typesafe.errors import NotATypeError, InvalidTypeError, UnlabeledArgError
import inspect


# decorators
def types(**kwargs):
    intended_types = kwargs
    intended_types['self'] = Any
    
    for var_name, var_type in intended_types.items():
        if not inspect.isclass(var_type):
            raise NotATypeError(var_type)
    
    def decorator(function):
        var_names = function.func_code.co_varnames
        for var_name in var_names:
            if var_name == '_':
                continue
                
            if var_name not in intended_types.keys():
                raise UnlabeledArgError(var_name)
        
        def wrapper(*args, **kwargs):
            received_args = {}
            for index, arg_val in enumerate(args):
                received_args[var_names[index]] = arg_val
            received_args.update(kwargs)
            
            for var_name, arg_val in received_args.items():
                var_type = intended_types[var_name]
                if var_type is Any:
                    continue
                
                if not isinstance(arg_val, var_type):
                    raise InvalidTypeError(var_name, arg_val, var_type)
            
            return function(*args, **kwargs)
        
        return wrapper
        
    return decorator

def returns(ret_type):
    if not inspect.isclass(ret_type):
        raise NotATypeError(ret_type)
    
    def decorator(function):
        if ret_type is Any:
            return function
        
        def wrapper(*args, **kwargs):
            ret_val = function(*args, **kwargs)
            if not isinstance(ret_val, ret_type):
                raise InvalidTypeError('returned value', ret_val, ret_type)
            return ret_val
        
        return wrapper
    
    return decorator