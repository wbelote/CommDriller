import sqlite3


def query(f):
    def full():
        db = sqlite3.connect("comms.db")
        f(db.cursor())
        db.commit()
        db.close()

    return full


schema = """
DROP TABLE IF EXISTS Cases;
CREATE TABLE Cases (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    type    INTEGER NOT NULL,
    buffer  INTEGER NOT NULL,
    target1 INTEGER NOT NULL,
    target2 INTEGER NOT NULL,
    alg TEXT NOT NULL
);

DROP TABLE IF EXISTS Times;
CREATE TABLE Times (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    time  NUMERIC NOT NULL,
    date  TEXT,
    case_id   NUMERIC
);

DROP TABLE IF EXISTS Locations;
CREATE TABLE Locations (
    id    INTEGER NOT NULL PRIMARY KEY UNIQUE,
    faces TEXT NOT NULL UNIQUE,
    letter    TEXT NOT NULL
);
"""

default_data = ""

# Location data
edges = "UB UR UF UL LU LF LD LB FU FR FD FL RU RB RD RF BU BL BD BR DF DR DB DL".split()
corners = "UBL URB UFR ULF LUB LFU LDF LBD FUL FRU FDR FLD RUF RBU RDB RFD BUR BLU BDL BRD DFL DRF DBR DLB".split()
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
loc_id = {}
for i in range(24):
    loc_id[corners[i]] = 2 * i + 1
    default_data += f"INSERT INTO Locations(faces, letter) VALUES ('{corners[i]}', '{letters[i]}');\n"
    loc_id[edges[i]] = 2 * i + 2
    default_data += f"INSERT INTO Locations(faces, letter) VALUES ('{edges[i]}', '{letters[i]}');\n"


# Comms from Daniel's sheet
def invert(alg):
    if "[" in alg:
        b1 = alg.index("[") + 1
        b2 = alg.rindex("]")
        return alg[:b1] + invert(alg[b1:b2]) + alg[b2:]

    if "(" in alg:
        b1 = alg.index("(") + 1
        b2 = alg.rindex(")")
        return alg[:b1] + invert(alg[b1:b2]) + alg[b2:]

    if "," in alg:
        parts = alg.split(",")
        return f"{parts[1].strip()}, {parts[0]}"

    out = ""
    for m in alg.split()[::-1]:
        if m[-1] == "'":
            out += m[:-1] + " "
        else:
            out += m + "' "
    return out


with open("comms-corners.tsv") as table:
    firsts = table.readline().strip("\n").split("\t")[1:]
    # print(firsts)
    comms = {p: {} for p in firsts}
    for i in range(24):
        line = table.readline().strip("\n").split("\t")
        # print(f"##########\n{i}\n{line}\n###########\n")
        second = line.pop(0)
        for j in filter(lambda x: line[x] not in {"", "twist", "flip"}, range(24)):
            # print(i, j, firsts[j], second, line[j], invert(line[j]))
            # print(f"-----------\n{i} {j}\n\tt1: {firsts[j]}\n\tt2: {second}\n"
            #       f"\tnormal: {line[j]}\n\tinverse: {invert(line[j])}\n------\n")
            comms[firsts[j]][second] = line[j]
            comms[second][firsts[j]] = invert(line[j])
            normal = line[j].replace("'", "''")
            inverse = invert(line[j]).replace("'", "''")
            default_data += "INSERT INTO Cases(type, buffer, target1, target2, alg)" \
                            f" VALUES(1, 5, {loc_id[firsts[j]]}, {loc_id[second]}, '{normal}');\n"
            default_data += "INSERT INTO Cases(type, buffer, target1, target2, alg)" \
                            f" VALUES(1, 5, {loc_id[second]}, {loc_id[firsts[j]]}, '{inverse}');\n"


@query
def setup(c):
    c.executescript(schema)
    for q in default_data.split("\n"):
        print(q)
        c.executescript(q)


if __name__ == '__main__':
    setup()
