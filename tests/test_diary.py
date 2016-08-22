import os
import sys
import mock
sys.path.append(os.path.realpath(".."))
import unittest
from pysqlcipher import dbapi2 as sqlite

from cli_diary.database import DBConnector
from cli_diary.diary import CLIUI

class testDiary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #connect to the database
        conn = sqlite.connect('test.db')
        c = conn.cursor()
        c.execute("PRAGMA key='pass'")
        #create the test database if it does not exist
        c.execute(
        """CREATE TABLE IF NOT EXISTS entries (id integer primary key
        autoincrement, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, title
        CHAR(50), content CHAR(2000))"""
        )
        #start with an empty table for tests
        c.execute("""DELETE FROM entries""")
        conn.commit()
        c.close()
        conn.close()

        #the database connector that we are going to test
        cls.dbconn = DBConnector('./test.db','pass')

    @classmethod
    def setUp(cls):
        conn = sqlite.connect('test.db')
        c = conn.cursor()
        c.execute("PRAGMA key='pass'")
        c.execute("""DELETE FROM entries""")
        conn.commit()
        c.close()
        conn.close()
        return

    def testCreateEntry(self):
        with mock.patch.object(CLIUI, 'promptForEntry', return_value=("hi","hello")) as mock_method:
            db = "test.db"
            password = "pass"
            ui = CLIUI(db, password)
            ui.createEntry()
        # TODO: Move this server connection stuff into a function
        conn = sqlite.connect('test.db')
        c = conn.cursor()
        c.execute("PRAGMA key='pass'")
        entries = c.execute("SELECT * FROM entries").fetchall()
        c.close()
        conn.close()
        self.assertEqual(1,len(entries))
        self.assertEqual("hi", entries[0][2])
        self.assertEqual("hello", entries[0][3])
        return

    def testSelectEntryNone(self):
        with mock.patch.object(CLIUI, 'promptForInput', return_value="q") as mock_method:
            db = "test.db"
            password = "pass"
            ui = CLIUI(db, password)
            result = ui.selectEntry()
            self.assertEqual(0, len(result))
            self.assertEqual([], result)
            return

    def testSelectEntryOne(self):
        db = "test.db"
        password = "pass"
        conn = sqlite.connect(db)
        c = conn.cursor()
        c.execute("PRAGMA key='{}'".format(password))
        sql_query="INSERT INTO entries (title, content) VALUES (\'Hi\',\'Bye\')"
        c.execute(sql_query)
        c.close()
        conn.commit() # AHH
        conn.close()
        with mock.patch.object(CLIUI, 'promptForInput', return_value=0) as mock_method:
            ui = CLIUI(db, password)
            return
            result = ui.selectEntry()
            self.assertEqual(4, len(result))
            self.assertEqual('Hi', result[2])
            self.assertEqual('Bye', result[3])

    @classmethod
    def tearDownClass(cls):
        cls.dbconn.close()

if __name__ == "__main__":
    unittest.main()
