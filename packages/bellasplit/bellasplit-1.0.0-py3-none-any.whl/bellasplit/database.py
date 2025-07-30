import os
from os.path import join as _j
from typing import List, Tuple
from pamly import Diagnosis, Stain

from bellameta.utils import sqlite_connection, get_env
from bellameta.types import Cohort, Task
from bellameta.constants import METADATA_TABLES

from bellasplit.types import Mode, Splitname
from bellasplit.filter import Filter
from bellasplit import constants

class Db:
    '''
    Class to manage connection to database holding scans and their metadata

    Attributes
    ----------
    sqlite_path: str
        Absolute path to the sqlite database holding storage table of WSI scans
    '''   
     
    def __init__(self, sqlite_path: str | None = None):
        if sqlite_path is None:
            self.sqlite_path = constants.DB_PATH
        else:
            self.sqlite_path = sqlite_path
        self._initialize_db('mode', 'TEXT')
        self._initialize_db('split', 'TEXT')
        
    @sqlite_connection
    def _table_exists(self, cursor, table_name: str):
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE name=?", (table_name, ))
        result = cursor.fetchall()
        if result:
            return True
        else:
            False

    @sqlite_connection
    def _initialize_db(self, cursor, table_name, type = 'TEXT'):
        if not self._table_exists(table_name):
            cursor.execute(self.create_statement(table_name, type))
    
    @staticmethod
    def create_statement(table_name: str, type = 'TEXT'):
        '''
        Helper method to form sqlite statements for table creation
        '''

        if table_name == 'mode':
            statement = f'''CREATE TABLE {table_name} (
                        hash TEXT,
                        value {type},
                        split TEXT,
                        FOREIGN KEY(hash) REFERENCES storage(hash)
                        )'''
            return statement
        statement = f'''CREATE TABLE {table_name} (
                    hash TEXT,
                    value {type},
                    FOREIGN KEY(hash) REFERENCES storage(hash)
                    )'''
        return(statement)