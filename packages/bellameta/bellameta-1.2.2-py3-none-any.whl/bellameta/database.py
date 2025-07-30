from os.path import join as _j
from typing import List, Tuple
import sqlite3 
import pandas as pd

from bellameta.utils import sqlite_connection
from bellameta import constants



def create_statement(table_name: str, type = 'TEXT'):
    statement = f'''CREATE TABLE {table_name} (
                hash TEXT,
                value {type},
                UNIQUE(hash, value),
                FOREIGN KEY(hash) REFERENCES storage(hash)
                )'''
    return statement

class Db():
    '''
    Class to manage metadata within sqlite table

    Attributes
    ----------
    sqlite_path: str
        Absolute path to the sqlite database holding storage table of WSI scans
    tables: List[str]
        Names of metadata tables to be initialized/modified

    Methods
    -------
    write:
        Method to write metadata as key (hash) value pair into the specified metadata table
    write_many:
        Bulk insert of metadata into the specified metadata table
    '''

    def __init__(self, sqlite_path: str | None = None, tables = constants.METADATA_TABLES):
        if sqlite_path is None:
            self.sqlite_path = constants.DB_PATH
        else:
            self.sqlite_path = sqlite_path
        self.tables = tables
        self._initialize_db()

    @sqlite_connection
    def _initialize_db(self, cursor):
        existing_tables = []
        for table_name in self.tables:
            if not self._table_exists(table_name):
                print(f'Creating table {table_name}')
                cursor.execute(create_statement(table_name))
            else:
                existing_tables.append(table_name)
        print(f'Already existing metdata tables: {existing_tables}')

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
    def drop_all_metadata_tables(self, cursor):
        '''
        This is just a utility function that should normally not be used
        '''

        for table in self.tables:
            cursor.execute(f'''DELETE FROM {table}''')
                
    @sqlite_connection
    def write(self, cursor, hash: str, value: str, table_name: str):
        '''
        Method to write metadata as key (hash) value pair into the specified metadata table

        Parameters
        ----------
        hash : str
            Hash of WSI scan, serving as unique key in the database
        value : str
            metadata value
        table_name : str
            name of the metadata table to be inserted to
        '''

        if value:
            cursor.execute(
                f"INSERT OR IGNORE INTO {table_name} (hash, value) VALUES (?, ?)",
                (hash, value)
            )
    @sqlite_connection
    def write_many(self, cursor, data: List[Tuple], table_name):
        '''
        Bulk insert of metadata into the specified metadata table
        '''

        # validation
        filtered_data = [(hash, value) for (hash, value) in data if value is not None]
        cursor.executemany(
            f"INSERT OR IGNORE INTO {table_name} (hash, value) VALUES (?, ?)",
            filtered_data
        )
    
    def read_pd(self, table_name: str, rows: int | None = 5):
        '''
        Reads in the first rows of the table as pandas dataframe 
        '''

        conn = sqlite3.connect(self.sqlite_path)
        statement = f"SELECT * FROM {table_name}"
        if rows is not None:
            statement += f" LIMIT {rows}"
        df = pd.read_sql_query(statement, conn)
        conn.close()
        return df
    
    def __str__(self):
        out = ""
        for table_name in self.tables:
            df = self.read_pd(table_name, rows=5)
            out += f"Table {table_name}:\n {df.to_string()}\n"
        return(out)
    

                
            

