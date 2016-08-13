import sys
sys.path.append("/home/harris/Documents/cli_diary")
import unittest
from pysqlcipher import dbapi2 as sqlite
conn = sqlite.connect('test.db')
c = conn.cursor()
c.execute("PRAGMA key='test'")

from cli_diary.database import DBConnector

class testDBConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #connect to the database
        conn = sqlite.connect('test.db')
        c = conn.cursor()
        c.execute("PRAGMA key='pass'")
        #create the test database if it does not exist
        c.execute("""CREATE TABLE IF NOT EXISTS entries (id integer primary key autoincrement, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, title CHAR(50), content CHAR(2000))""")
        #start with an empty table for tests
        c.execute("""DELETE FROM entries""")
        conn.commit()
        c.close()

        #the database connector that we are going to test
        cls.dbconn = DBConnector('./test.db','pass')

    def testAddAnEntry(self):
        new_title = "New Title for Entry"
        new_content = "New content for entry."
        self.dbconn.insert(title=new_title, content=new_content)

        conn = sqlite.connect('test.db')
        c = conn.cursor()
        c.execute("PRAGMA key='pass'")
        new_entry = c.execute("""select title, content from entries""").fetchall()
        c.close()

        self.assertEqual(1, len(new_entry))
        self.assertEqual(2, len(new_entry[0]))
        self.assertEqual(new_title, new_entry[0][0])
        self.assertEqual(new_content, new_entry[0][1])

    @classmethod
    def tearDownClass(cls):
        cls.dbconn.close()

if __name__ == "__main__":
    unittest.main()
