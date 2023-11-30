import os
from datetime import datetime
import pymysql

class Cursor:

    def __init__(self, host='localhost', port=3306, user='root', passwd='password', db_name=None, table_name=None):

        self.login = {
                "host" : os.getenv('LAZYINS_HOST') if os.getenv('LAZYINS_HOST') else host,
                "port" : int(os.getenv('LAZYINS_PORT')) if os.getenv('LAZYINS_PORT') else port,
                "user" : os.getenv('LAZYINS_USER') if os.getenv('LAZYINS_USER') else user,
                "passwd" : os.getenv('LAZYINS_PASSWD') if os.getenv('LAZYINS_PASSWD') else passwd,
                "autocommit" : True
                }
        self.conn = pymysql.connect(**self.login)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

        self.db_name = db_name if db_name else 'dummy_dababase'
        self.table_name = table_name if table_name else 'dummy_table'

        self.names = None
        self.types = None
        self.default_char_length = 40
        self.before_initial_execute = True


    def setup(self, names=None, values=None, types=None, explicit_types=[]):

        if names != None:
            self.names = names
        if types != None:
            self.types = types

        if self.names == None:
            print('Column names are unknown.')
            return

        if values != None:
            self.types = self.guess_types(values)

        if len(self.names) != len(self.types):
            print('Numbers of names and types are not match.')
            return

        if 'unknown' in l:
            print('Unknown type(s) are included.')
            return

        for e in explicit_types:
            index = names.index(e[0])
            self.types[index] = e[1]


        self.table_query = 'CREATE TABLE IF NOT EXISTS {} '.format(self.table_name)
        self.table_query += '(id int auto_increment, time TIMESTAMP not null default CURRENT_TIMESTAMP,'        

        for n, t in zip(self.names, self.types):
            self.table_query += ' {} {},'.format(n, t)

        self.table_query += ' PRIMARY KEY (id));'

        insert_query = 'INSERT INTO {} ('.format(self.table_name)
        for c in names:
            insert_query += c + ','
        insert_query = insert_query[:-1] + ')'
        insert_query += ' VALUES (' + '%s,' * len(names)
        self.insert_query = insert_query[:-1] + ')'

        
        print(self.table_name)
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(self.db_name))
        self.cursor.execute("USE {};".format(self.db_name))
        self.cursor.execute(self.table_query)

        self.before_initial_execute = False


    def register(self, values, names=None, explicit_types=[]):

        # unpack list of tuple : [('name1', 1), ('name2', 2)]
        if type(values[0]) == tuple:
            names = [v[0] for v in values]
            values = [v[1] for v in values]

        if self.before_initial_execute:
            self.setup(names, values, explicit_types=explicit_types)

        self.cursor.execute(self.insert_query, tuple(values))


    def guess_types(self, values):
        types = []
        for v in values:
            if type(v) == int:
                type_ = 'int'
            elif type(v) == float:
                type_ = 'float'
            elif type(v) == bool:
                type_ = 'bool'
            elif type(v) == str:
                type_ = 'varchar({})'.format(self.default_char_length)
            elif type(v) == datetime:
                type_ = 'datetime'
            else :
                type_ = 'unknown'
            types.append(type_)
        return types


