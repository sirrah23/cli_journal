import os
import sys
import mock
import utils
sys.path.append(os.path.realpath(".."))
import unittest
from pysqlcipher import dbapi2 as sqlite
from cli_diary.diary import CLIUI

db='test.db'
password='pass'

class testDiary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.createAndEmptyEntries(db,password)

    @classmethod
    def setUp(cls):
        utils.emptyEntries(db, password)

    def testCreateEntry(self):
        with mock.patch.object(CLIUI, 'promptForEntry', return_value=("hi","hello")) as mock_method:
            ui = CLIUI(db, password)
            ui.createEntry()
        entries = utils.getEntries(db, password)
        self.assertEqual(1,len(entries))
        self.assertEqual("hi", entries[0][2])
        self.assertEqual("hello", entries[0][3])
        return

    def testCreateEntryNone(self):
        with mock.patch.object(CLIUI, 'promptForEntry', return_value=("","")) as mock_method:
            ui = CLIUI(db, password)
            ui.createEntry()
        entries = utils.getEntries(db, password)
        self.assertEqual(0,len(entries))

    def testSelectEntryNone(self):
        with mock.patch.object(CLIUI, 'promptForInput', return_value="q") as mock_method:
            ui = CLIUI(db, password)
            result = ui.selectEntry()
            self.assertEqual(0, len(result))
            self.assertEqual([], result)
            return

    def testSelectEntryOne(self):
        utils.insertEntry(db,password,'Hi','Bye')
        with mock.patch.object(CLIUI, 'promptForInput', return_value=0) as mock_method:
            ui = CLIUI(db, password)
            result = ui.selectEntry()
            self.assertEqual(4, len(result))
            self.assertEqual('Hi', result[2])
            self.assertEqual('Bye', result[3])
            return

    def testDeleteEntry(self):
        # Insert an entry
        utils.insertEntry(db,password,'Hi','Bye')
        # Get the id of the inserted entry
        entries = utils.getEntries(db, password)
        inserted_id = entries[0][0]
        # Perform deletion
        ui = CLIUI(db, password)
        ui.deleteEntry(inserted_id)
        # Check to see that it worked
        entries = utils.getEntries(db, password)
        self.assertEqual(0, len(entries))
        return

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
