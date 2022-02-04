import mysql.connector
from .Constant import *
import discord
from discord.ext import commands

class UserDbError(commands.CommandError):
    pass

class DatabaseNotExist(UserDbError):
    pass

def _is_database_exist(cursor):
    cursor.execute("""SHOW DATABASES LIKE '{}'""".format(DB_NAME))
    x = [i for i in cursor]
    if len(x) == 0:
        raise DatabaseNotExist

    return SUCCESS

def connect():
    mydb = mysql.connector.connect(
        host = HOST_NAME,
        user = USER_NAME,
        password = PASSWORD)

    return mydb

def get_cursor(mydb, dict_cursor = False):
    if dict_cursor:
        cursor = mydb.cursor(dictionary=True)
    else:
        cursor = mydb.cursor()

    if _is_database_exist(cursor):
        cursor.execute("USE {};".format(DB_NAME))
        return cursor

class UserDbConn:
    def __init__ (self):
        self.db = connect()
        self.cur = get_cursor(self.db, True)
        self.create_tables()

    def create_tables(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS user_handle('
            'user_id BIGINT,'
            'guild_id BIGINT,'
            'handle TEXT,'
            'PRIMARY KEY (user_id, guild_id)'
            ')'
        )
        self.db.commit()

    def insert(self, table, fields, values: tuple):
        n = len(values)
        query = '''
            INSERT INTO {} ({}) VALUES ({});
            '''.format(table, ', '.join(fields), ', '.join(['%s'] * n))
        self.cur.execute(query, values)
        self.db.commit()
        

        
        
        
