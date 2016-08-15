from database import DBConnector

class CLIUI:

    def __init__(self, password):
        self.db = "diary.db"
        self.dbconn = DBConnector(self.db, password)

    def mainLoop(self):
        print """
        Welcome to your diary! Write down your secret thoughts, they will be safe here!

        What would you like to do?

        1) Create a new entry
        2) View all entries
        3) Delete an entry
        4) Quit

        """
        choice = 0
        while choice != 4:
            try:
                choice = int(raw_input("Selection: "))
            except:
                print "Bad selection! Try something else!"
                continue

            if choice == 1:
                # TODO: Code for creating an entry
                pass
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
