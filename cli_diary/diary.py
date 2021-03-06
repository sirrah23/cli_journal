from database import DBConnector
import sys
import getpass
import sys, tempfile, os
from subprocess import call

class CLIUI:

    def __init__(self, db, password):
        self.db = db
        self.dbconn = DBConnector(self.db, password)

    def promptForEntry(self):
        """Obtain user's input for the diary entry from the terminal via their favorite text editor."""
        EDITOR = os.environ.get('EDITOR','vim') # Grab the user's favorite editor, vim by default...
        initial_message = "Write your entry here! The first line will be your title!" # input setup

        # Input file where user will type their entry
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.write(initial_message)
            tf.flush()
            call([EDITOR, tf.name])

            # Get the entry!
            tf.seek(0)
            edited_message = tf.readlines()

            # Get rid of initial template message if it was not erased
            if edited_message[0] == initial_message + '\n':
                edited_message.pop(0)
            title = content = ""
            # Split entry into title and content if user supplied an entry
            if len(edited_message) >= 2:
                title = edited_message.pop(0)     # Title is the first line
                content = ''.join(edited_message) # remaining lines are diary content
        return title, content

    def promptForInput(self, inputMessage):
        """Prompts the user for input."""
        user_input = raw_input(inputMessage)
        return user_input

    def createEntry(self):
        """Get the user's diary entry and put it into the database."""
        title, content = self.promptForEntry()
        # If no input supplied then don't save anything to database
        if len(title) == 0 or len(content) == 0:
            print "\n"
            print "Nothing was saved!"
        else:
            self.dbconn.insert(title, content)
            print "\n"
            print "Diary entry saved successfully!"
        return

    def selectEntry(self):
        """Allow the user to select an entry and return the corresponding entry from SQL table"""
        entries = self.dbconn.getAllEntries()
        titles = map(lambda entry: entry[2], entries)
        for i in range(len(titles)):
            print str(i) + "." + titles[i]
        result = None
        while result == None:
            print "Select an entry, or type q to quit."
            selection = self.promptForInput("> ")
            try:
                selection = int(selection)
                if selection in range(len(titles)):
                    result = entries[selection]
                else:
                    result = None
                    print "Try again!"
            except:
                if selection == "q" or selection == '':
                    result = []
                else:
                    result = None
                    print "Try again!"
        return result

    def deleteEntry(self, id_to_delete):
        """Given the id for a diary entry, the diary entry will be deleted."""
        self.dbconn.deleteEntryByID(id_to_delete)
        return

    def passwordIsCorrect(self):
        """Returns True if the password is correct, otherwise False."""
        return self.dbconn.isThePasswordCorrect()

    def mainLoop(self):
        print "Welcome to your diary! Write down your secret thoughts, they will be safe here!"

        choice = 0
        while choice != 4:
            print """
            What would you like to do?

            1) Create a new entry
            2) View an entry
            3) Delete an entry
            4) Quit
            """
            try:
                choice = int(self.promptForInput("Selection: "))
            except:
                print "Bad selection! Try something else!"
                continue
            if choice == 1:
                self.createEntry()
            elif choice == 2:
                entry = self.selectEntry()
                if entry == []:
                    continue
                else:
                    # Print title and content
                    print entry[2]
                    print entry[3]
                    self.promptForInput("Press RETURN when finished.")
            elif choice == 3:
                entry = self.selectEntry()
                if entry == []:
                    continue
                else:
                    id_to_delete=entry[0]
                    self.deleteEntry(id_to_delete)
                    self.promptForInput("Entry has been deleted. Press RETURN.")
            elif choice == 4:
                pass
            else:
                print "Bad selection! Try something else!"
        print "See you later! <3"
        return

if __name__ == "__main__":
    database="diary.db"
    print "Password?"
    password = getpass.getpass("> ")
    ui = CLIUI(database,password)
    if not ui.passwordIsCorrect():
        print "Go away."
    else:
        ui.mainLoop()
