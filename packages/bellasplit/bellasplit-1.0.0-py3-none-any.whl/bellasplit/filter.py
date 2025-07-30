from typing import Type, List
from bellameta.types import BellametaType

from bellasplit.utils import validate_table_name

class Filter():
    '''
    Class defining a filter to retrieve entries of a table satisfying a search condition

    Parameters
    ----------
    table_name: str
        The name of the table in the database
    value: Type[BellametaType] | List[Type[BellametaType]]
        The value specifying the search condition

    Attributes
    -------
    values:
        The list of values specifying the search condition
    table:
        Equals table_name parameter
    placeholder:
        sqlite placeholder to be used in WHERE condition
    
    Raises
    ------
    ValueError if validation of table_name fails
    ValueError if value is of wrong type
    '''

    def __init__(self,
                 table_name: str,
                 value: Type[BellametaType] | List[Type[BellametaType]]):
        self.name = validate_table_name(table_name)
        if not isinstance(value, list):
            value = [value]
        try:
            value = [v.to_string() for v in value]
        except:
            raise ValueError(f'The provided value {value} is not of type BellametaType.')
        self.values = value
        self.table = table_name
        self.placeholder = ','.join('?' * len(self.values))

        
        



        
        
        
        

        
        
        
        
        