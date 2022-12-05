import sqlite3
from pprint import *


def main():

    con = sqlite3.connect("jeopardy.db")
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE jeopardy_copy (
        id INTEGER PRIMARY KEY autoincrement,
        value INTEGER,
        category TEXT,
        question TEXT,
        answer TEXT)""")
    cur.execute(
        """INSERT INTO jeopardy_copy
        VALUES (value, category, question, answer)
        SELECT CAST(value as integer), category, question, answer""")

    con.commit()
    con.close()


main()
