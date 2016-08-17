from database import DBConnector
import sys

class CLIUI:

    def __init__(self, password):
        self.db = "diary.db"
        self.dbconn = DBConnector(self.db, password)

    def getUserInput(self):
        """Obtain user's input for the diary entry from the terminal."""
        print "Start typing an entry."
        print "----------------------"
        content = sys.stdin.readlines()[0]
        print "\n"
        print "Title?"
        print "------"
        title = sys.stdin.readlines()[0]
        return title, content

    def createEntry(self):
        """Get the user's diary entry and put it into the database."""
        title, content = self.getUserInput()
        self.dbconn.insert(title, content)
        print "\n"
        print "Diary entry saved successfully!"
        return

    def mainLoop(self):
        print "Welcome to your diary! Write down your secret thoughts, they will be safe here!"

        choice = 0
        while choice != 4:
            print """
            What would you like to do?

            1) Create a new entry
            2) View all entries
            3) Delete an entry
            4) Quit
            """
            try:
                choice = int(raw_input("Selection: "))
            except:
                print "Bad selection! Try something else!"
                continue

            if choice == 1:
                self.createEntry()
            elif choice == 2:
                # TODO: Code for viewing all entries
                pass
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
    password = "password123"
    ui = CLIUI(password)
    ui.mainLoop()
