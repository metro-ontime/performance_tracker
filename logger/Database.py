import sqlite3
import os

class Database:
    def __init__(self, name):
        while True:
            try:
                conn = sqlite3.connect(name)
                break
            except:
                os.remove(name)
                new_file = open(name, 'w+')
                new_file.close()

        self.cursor = conn.cursor()
        self.connection = conn

    def execute(self, query):
        self.cursor.execute(query)
    
    def save_and_close(self):
        self.connection.commit()
        self.connection.close()
