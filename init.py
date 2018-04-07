import sqlite3
conn = sqlite3.connect("strategy.db")
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")

c.execute("DROP TABLE IF EXISTS beads;")
c.execute("""CREATE TABLE beads(
                 gameboard TEXT NOT NULL,
                 column0 integer NOT NULL DEFAULT 10,
                 column1 integer NOT NULL DEFAULT 10,
                 column2 integer NOT NULL DEFAULT 10,
                 column3 integer NOT NULL DEFAULT 10,
                 column4 integer NOT NULL DEFAULT 10,
                 column5 integer NOT NULL DEFAULT 10,
                 column6 integer NOT NULL DEFAULT 10,
                 PRIMARY KEY (gameboard));""")

conn.commit()
conn.close()
