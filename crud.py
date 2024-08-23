import os
import sys
import psycopg2
import psycopg2.sql as sql
from dotenv import load_dotenv
import bcrypt
import binascii
load_dotenv()

class Crud:
    def __init__(self, table, primarykey):
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT')
        self.dbname = os.getenv('DB_NAME')
        self.table = table
        self.primarykey = primarykey

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                port=self.port,
                dbname=self.dbname
            )
            self._cursor = self._connection.cursor()
            print('PostgreSQL connected')
        except (Exception, psycopg2.Error) as error:
            print(error, error.pgcode, error.pgerror, sep='\n')
            sys.exit()

    def _execute(self, query, Placeholder_value=None):
        if Placeholder_value is None or None in Placeholder_value:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, Placeholder_value)

    def insert(self, **column_value):
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join(map(sql.Identifier, column_value.keys())),
            sql.SQL(', ').join(sql.Placeholder() * len(column_value.values()))
        )
        record_to_insert = tuple(column_value.values())
        self._execute(insert_query, record_to_insert)

    def select(self, columns, primaryKey_value=None):
     print(f"Primary Key Value Type: {type(primaryKey_value)}")  # Debugging line
     if primaryKey_value is None:
        select_query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(self.table)
        )
        self._execute(select_query)
     else:
        select_query = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(self.table),
            sql.Identifier(self.primarykey)
        )
        self._execute(select_query, (primaryKey_value,))
     return self._cursor.fetchall()
 

    def create_user(self,id, username, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.insert(id=id,username=username, password=hashed)
        print(f"User {username} created with hashed password.")


    def validate_user(self, username, password):
   
     select_query = sql.SQL("SELECT password, id FROM {} WHERE username = %s").format(
        sql.Identifier(self.table)
     )
     self._execute(select_query, (username,))
     result = self._cursor.fetchone()
    
     if result:
        stored_password_hex, user_id = result
        
   
        stored_password = binascii.unhexlify(stored_password_hex[2:])
        
       
        print(f"Retrieved stored_password type: {type(stored_password)}, value: {stored_password}")
        print(f"Retrieved user_id type: {type(user_id)}, value: {user_id}")

       
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print(f"User {username} validated successfully.")
            return user_id  
        else:
            print(f"Invalid password for user {username}.")
     else:
        print(f"User {username} not found.")
     return None

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()
