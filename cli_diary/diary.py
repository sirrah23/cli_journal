from database import DBConnector
import sys

class CLIUI:

    def __init__(self, db, password):
        self.db = db
        self.dbconn = DBConnector(self.db, password)

    def promptForEntry(self):
        """Obtain user's input for the diary entry from the terminal."""
        print "Start typing an entry."
        print "----------------------"
        content = sys.stdin.readlines()[0]
        print "\n"
        print "Title?"
        print "------"
        title = sys.stdin.readlines()[0]
        return title, content

    def promptForInput(self, inputMessage):
        """Prompts the user for input."""
        user_input = raw_input(inputMessage)
        return user_input

    def createEntry(self):
        """Get the user's diary entry and put it into the database."""
        title, content = self.promptForEntry()
        self.dbconn.insert(title, content)
        print "\n"
        print "Diary entry saved successfully!"
        return

    def selectEntry(self):
        """Allow the user to select an entry and return the corresponding entry from SQL table"""
        entries = self.dbconn.getAllEntries()
        titles = map(lambda entry: entry[3], entries)
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
                if selection == "q":
                    result = []
                else:
                    result = None
                    print "Try again!"
        return result

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
                # TODO: Code for deleting an entry
                pass
            elif choice == 4:
                pass
            else:
                print "Bad selection! Try something else!"
        print "See you later! <3"
        return

if __name__ == "__main__":
    database="diary.db"
    password = "password123"
    ui = CLIUI(database,password)
    ui.mainLoop()
