import sqlite3

db = sqlite3.connect("comms.db")
c = db.cursor()

schema = """
CREATE TABLE "Cases" (
    "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "buffer"    TEXT NOT NULL,
    "target1"    TEXT NOT NULL,
    "target2"    TEXT NOT NULL,
    "alg"   TEXT NOT NULL
);

CREATE TABLE "Times" (
    "id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "time"  NUMERIC NOT NULL,
    "date" TEXT,
    case_id NUMERIC
);
"""

c.execute(schema)
db.commit()

c.close()
db.close()
