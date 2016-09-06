import os
import sys
import utils
sys.path.append(os.path.realpath(".."))
import unittest
from pysqlcipher import dbapi2 as sqlite

from cli_diary.database import DBConnector

db="test.db"
password="pass"

class testDBConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the table if it does not exist and clear entries table
        utils.createAndEmptyEntries(db,password)
        #the database connector that we are going to test
        cls.dbconn = DBConnector('./'+db,password)

    @classmethod
    def setUp(cls):
        # Clear the database before each test
        utils.emptyEntries(db, password)
        return

    def testAddAnEntry(self):
        # Insert into the database
        new_title = "New Title for Entry"
        new_content = "New content for entry."
        self.dbconn.insert(title=new_title, content=new_content)

        # Get all the entries in the database
        new_entry = utils.getEntries(db, password)

        # Assert that our insertion is reflected in the database
        self.assertEqual(1, len(new_entry))
        self.assertEqual(4, len(new_entry[0]))
        self.assertEqual(new_title, new_entry[0][2])
        self.assertEqual(new_content, new_entry[0][3])

    def testAddAnEntryComma(self):
        # Insert an entry into the database that has commas in it! 
        new_title = "New Title for Entry"
        new_content = "New content for entry. Let's see if commas work!."
        self.dbconn.insert(title=new_title, content=new_content)

        # Get all the entries in the database
        new_entry = utils.getEntries(db, password)

        # Assert that our insertion is reflected in the database
        self.assertEqual(1, len(new_entry))
        self.assertEqual(4, len(new_entry[0]))
        self.assertEqual(new_title, new_entry[0][2])
        self.assertEqual(new_content, new_entry[0][3])

    def testViewAllEntries(self):
        # Database should be empty to start with
        entries = self.dbconn.getAllEntries()
        self.assertEqual(0, len(entries))
        self.dbconn.insert(title="t1", content="c1\n")
        # Adding one item, should be able to see it
        entries = self.dbconn.getAllEntries()
        self.assertEqual(1, len(entries))
        self.dbconn.insert(title="t2", content="c2\n")
        self.dbconn.insert(title="t3", content="c3\n")
        # Should be able to see three total at the end of insertions...
        entries = self.dbconn.getAllEntries()
        self.assertEqual(3, len(entries))

    def testDeleteEntry(self):
        # Populate entries table - SETUP
        utils.insertEntry(db, password, "T1", "C1")
        utils.insertEntry(db, password, "T2", "C2")

        # Pick entry to delete
        entries = utils.getEntries(db, password)
        titles = map(lambda e: e[2], entries)
        titleToDelete = titles[0] # going to delete the first entry from the datbase
        idToDelete = entries[0][0]

        # Perform delete
        self.dbconn.deleteEntryByID(idToDelete)
        # Recalculate entries
        entries = utils.getEntries(db, password)

        # Assertions
        self.assertEqual(1, len(entries))
        self.assertNotEqual(idToDelete, entries[0][0])
        self.assertNotEqual(titleToDelete, entries[0][3])
        return


    @classmethod
    def tearDownClass(cls):
        cls.dbconn.close()

if __name__ == "__main__":
    unittest.main()
