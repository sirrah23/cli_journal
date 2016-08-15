from pysqlcipher import dbapi2 as sqlite
import os

class DBConnector():

    def __init__(self, database_name, database_password):
        """Given a database name, connect to it! Use the given password to unencrypt it."""
        self.database_name = os.path.realpath(database_name)
        self.conn = sqlite.connect(self.database_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA key=\'{}\'".format(database_password))
        self.table = "entries"

    def insert(self, title, content):
        """Given the title and content for a new diary/journal entry, it will be inserted into the database's entries table."""
        sql_query="INSERT INTO {} (title, content) VALUES (\'{}\',\'{}\')".format(self.table,title, content)
        insert_result=self.cursor.execute(sql_query)
        self.conn.commit()

    def getAllEntries(self):
        """Will fetch everything in the entries table in the database and return a list of them."""
        sql_query = "SELECT * FROM {}".format(self.table)
        get_result = self.cursor.execute(sql_query).fetchall()
        return get_result

    def close(self):
        """End the connection to the sqlite table."""
        self.cursor.close()
        self.conn.close()
        return
