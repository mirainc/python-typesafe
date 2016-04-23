class NotATypeError(ValueError):
    def __init__(self, bad_type):
        str_val = "%r is not a valid type" % (bad_type)
        return super(ValueError, self).__init__(str_val)

     
class UnlabeledArgError(ValueError):
    def __init__(self, var_name):
        str_val = "%s does not have a specified type" % (var_name)
        return super(ValueError, self).__init__(str_val)


class InvalidTypeError(TypeError):
    def __init__(self, var_name, val, var_type):
        str_val = "%s (%r) is not type %s" % (var_name, val, var_type)
        return super(TypeError, self).__init__(str_val)