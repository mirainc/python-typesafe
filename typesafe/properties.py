# imports
from typesafe import types, Any


# properties
@types(property_key=str, property_type=Any)
def add_property(self, property_key, property_type):
    # adds a property() with the given type
    
    # expects a variable with the format "_property_name"
    # variables with the format "__property_name" will be
    #   obfuscated and unusable
    
    variable_key = '_' + property_key
    
    @types(returns=property_type)
    def __getter(self):
        return getattr(self, variable_key)
    
    @types(new_val=property_type)
    def __setter(self, new_val):
        setattr(self, variable_key, new_val)
    
    prop = property(__getter, __setter)
    setattr(self.__class__, property_key, prop)
