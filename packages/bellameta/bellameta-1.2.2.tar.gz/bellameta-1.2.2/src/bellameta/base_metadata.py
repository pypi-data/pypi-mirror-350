from typing import List
from abc import ABC, abstractmethod

from bellameta.utils import sqlite_connection
from bellameta.database import Db
from bellameta.types import Cohort, Task, Stain

class Metadata(ABC):
    '''
    Class that automates handling of metadata implemented in its child classes

    The beauty of this class is its dynamic definition of getter methods,
    based on metadata table names and the logic implemented in each child class.
    Each child class has to implement getters for the tables cohort, stain and task.

    Attributes
    ----------
    db: Db
        Database holding scans and metadata
    ingress_directory: str
        Absolute path of the original ingress directory that held scans BEFORE moving into storage.
        This is used to identify all scans of a single cohort.
    
    Methods
    -------
    get_hashes:
        Fetches all hashes of scans contained in original ingress directory (we think of this as a single cohort)
    get_scanname_from_hash:
        Returns the original scan name (not the hash) as specified by the clinic as stored in the storage table.
        Usually the scanname holds valuable metadata such as patient id, subtype, ... so this is the main source
        of metadata for further processing.
    write_many:
        Extends Db.write_many by using the dedicated getter methods of child class in order to preprocess data to be inserted
        into metadata tables.
    '''

    def __init__(self, db: Db, ingress_directory: str):

        self.db = db
        self.sqlite_path = db.sqlite_path
        self.ingress_directory = ingress_directory
        
        # This sets up getter methods for each table, returning None if not overwritten in child class
        def __getattr__(self, name):
            # Check if this is a get_* method
            if name.startswith('get_'):
                table = name[4:]  # Remove 'get_' prefix
                if table in self.db.tables:
                    return lambda hash, table=table: self._get_record(hash, table)
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if '__getattr__' not in self.__class__.__dict__:
            setattr(self.__class__, '__getattr__', __getattr__)

    def _get_record(self, hash, table):
        return None
    
    # this forces the user to implement the three main getter methods for cohort, stain and task
    @abstractmethod
    def get_cohort(self, hash) -> List[Cohort] | Cohort:
        '''
        If a list is returned a hash will have multiple entries in the cohort table.
        '''

        pass

    @abstractmethod
    def get_stain(self,hash) -> Stain:
        pass

    @abstractmethod
    def get_task(self, hash) -> List[Task] | Task:
        '''
        If a list is returned a hash will have multiple entries in the task table.
        '''

        pass

    @sqlite_connection
    def get_hashes(self, cursor):
        '''
        Fetches all hashes of scans contained in original ingress directory (we think of this as a single cohort)
        '''

        cursor.execute(f'''
                        SELECT hash FROM ingress
                        WHERE filepath GLOB '{self.ingress_directory}/*'
                       ''')
        data = cursor.fetchall()
        hashes = [entry[0] for entry in data]
        return hashes
    
    @sqlite_connection
    def get_scanname_from_hash(self, cursor, hash: str):
        '''
        Returns the original scan name (not the hash) as specified by the clinic as stored in the storage table.

        Usually the scanname holds valuable metadata such as patient id, subtype, ... so this is the main source
        of metadata for further processing.
        '''

        cursor.execute('''
                SELECT scanname FROM storage
                WHERE hash=?
                ''', (hash,))
        data = cursor.fetchone()
        return data[0]     
    
    def write_many(self):
        '''
        Extends Db.write_many by using the dedicated getter methods of child class in order to preprocess data to be inserted
        into metadata tables.

        This inserts all metadata into all metadata tables for which the child class
        implements the respective getter methods.

        If getter method returns list, there will be multiple entries for a hash in the respective metadata table
        '''

        hashes = self.get_hashes()
        for table in self.db.tables:
            method_name = f'get_{table}'
            get_method = getattr(self, method_name)
            data = []
            for hash in hashes:
                values = get_method(hash)
                if isinstance(values, List):
                    for value in values:
                        data.append((hash, value))
                else:
                    data.append((hash, values))
            self.db.write_many(data, table)
        