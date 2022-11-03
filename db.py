import sys
import apsw
from apsw import Error


def get_conn():
    try:
        conn = apsw.Connection('./tiny.sqlite')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id integer PRIMARY KEY, 
            sender TEXT NOT NULL,
            message TEXT NOT NULL);''')
        c.execute('''CREATE TABLE IF NOT EXISTS announcements (
            id integer PRIMARY KEY, 
            author TEXT NOT NULL,
            text TEXT NOT NULL);''')
        return conn
    except Error as e:
        print(e)
        sys.exit(1)
