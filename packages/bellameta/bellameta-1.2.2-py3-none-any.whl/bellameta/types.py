import abc
import pamly

from bellameta import constants
from bellameta.utils import get_config, custom_title

class BellametaType(type):
    ''' 
    A class representing the base metadata type serving as a blue print for child classes.

    Attributes
    ----------
    The attributes are dynamically set by the inheriting class.
    
    Methods
    -------
    from_str: 
        create class by providing a string (that is registered in the inheriting classe's value dict)
    from_int:
        create class by providing an integer (that is registered in the inheriting classe's value dict)
    list:
        list all values registered in the inheriting classe's value dict
    to_string:
        convert class into string (registered in inherting classe's value dict)
    
    '''

    def __new__(cls, s: str):
        return cls.from_str(s)

 
    def __init_subclass__(cls, values):
        super().__init_subclass__()
        if not hasattr(cls, 'values') or values:
            cls.values = values
            cls._key_map = {}
            for value in list(values.keys()):
                attr_name = custom_title(value.replace(" ", "_"))
                attr_value = type(f"{cls.__name__}{attr_name}", (), {
                    'to_string': classmethod(lambda cls, original_key=value: original_key),
                    # TODO: we do not use this anymore
                    'to_table_name': classmethod(lambda cls, original_key=value: original_key.lower())
                })
                # this is needed for proper inheritance, i.e., that e.g. Task.Subtyping also gets the labels class attribute
                for attr, val in cls.__dict__.items():
                    if not attr.startswith('__') and attr not in ['values', '_key_map'] and not callable(val):
                        setattr(attr_value, attr, val)
                setattr(cls, attr_name, attr_value)
                cls._key_map[attr_name] = value
    
    @classmethod
    def from_str(cls, s: str):
        clean = custom_title(s.replace(" ", "_"))
        if clean in vars(cls).keys():
            return getattr(cls, clean)
        else:
            raise ValueError(f"{s} is not a valid attribute.")     

        
    @classmethod
    def from_int(cls, i: int):
        value = list(cls.values.keys())[list(cls.values.values()).index(i)]
        return getattr(cls, value)
    
    @classmethod
    def list(cls):
        return list(cls.values.keys())

# Each new type can be specified via a new entry in the config_data yaml
class Cohort(BellametaType, values=constants.COHORTS):
    pass

class Task(BellametaType, values=constants.TASKS):
    @classmethod
    def to_label_table_name(cls):
        '''
        Mathod to map the task to its corresponding labels table
        '''
        
        return constants.LABEL_TABLE_NAME[cls.to_string()]
    pass

class Stain(BellametaType, values={k: v for v, k in enumerate([item.to_string() for item in pamly.Stain.list()])}):
    pass

class Subtype(BellametaType, values={k: v for v, k in enumerate([item.to_string() for item in pamly.Diagnosis.list()])}):
    pass


