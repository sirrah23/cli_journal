from pysqlcipher import dbapi2 as sqlite

"""Database utilities that are separate from the application
database connector. To be used for testing the functionality
without depending on the DBConn object."""

def createAndEmptyEntries(db, password):
    """Creates the entries table if it does not exist and empties the table."""
    #connect to the database
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute("PRAGMA key='{}'".format(password))
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
    return

def emptyEntries(db, password):
    """Empty the entries table. Clean table required for each test."""
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute("PRAGMA key='{}'".format(password))
    c.execute("""DELETE FROM entries""")
    conn.commit()
    c.close()
    conn.close()
    return

def getEntries(db, password):
    """Get everything in the database. Used a lot in testing stuff after insertions and deletions."""
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute("PRAGMA key='{}'".format(password))
    entries = c.execute("SELECT * FROM entries").fetchall()
    c.close()
    conn.close()
    return entries

def insertEntry(db, password, title, content):
    """Insert one entry into the entries table. Useful for testing database fetches."""
    conn = sqlite.connect(db)
    c = conn.cursor()
    c.execute("PRAGMA key='{}'".format(password))
    sql_query="INSERT INTO entries (title, content) VALUES (\'{}\',\'{}\')".format(title, content)
    c.execute(sql_query)
    c.close()
    conn.commit() 
    conn.close()
    return
