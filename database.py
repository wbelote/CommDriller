import random
import sqlite3


def query(f):
    def full(args=None):
        db = sqlite3.connect("comms.db")
        if args:
            result = f(db.cursor(), args)
        else:
            result = f(db.cursor())
        db.commit()
        db.close()
        return result

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
    date  INTEGER,
    case_id   INTEGER NOT NULL
);

DROP TABLE IF EXISTS Targets;
CREATE TABLE Targets (
    id    INTEGER NOT NULL PRIMARY KEY,
    type    INTEGER NOT NULL,
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
    loc_id[corners[i]] = i + 1
    default_data += f"INSERT INTO Targets(type, faces, letter) VALUES (1, '{corners[i]}', '{letters[i]}');\n"


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
    firsts = table.readline().replace("’", "'").replace("â€™", "'")
    firsts = firsts.strip("\n").split("\t")[1:]
    # print(firsts)
    comms = {p: {} for p in firsts}
    for i in range(24):
        line = table.readline().replace("’", "'").replace("â€™", "'")
        line = line.strip("\n").split("\t")
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
        # print(q)
        c.executescript(q)


class Case:
    def __init__(self, cols):
        self.id = cols[0]
        self.c = cols[1:5]
        self.target1 = [cols[1], cols[3]]
        self.target2 = [cols[2], cols[4]]
        self.cycle = f"UFR-{cols[1]}-{cols[2]} ({cols[3]}{cols[4]})"
        self.alg = cols[5]
        self.avg = cols[6]
        self.count = cols[7]


join_cases = """
SELECT  Cases.id
    ,   t1.faces AS faces1
    ,   t2.faces AS faces2
    ,   t1.letter AS letter1
    ,   t2.letter AS letter2
    ,   Cases.alg
    ,   TbAvg.t as avg_time
    ,   TbCount.n as time_count
FROM Cases
    LEFT JOIN Targets t1 ON t1.id = Cases.target1
    LEFT JOIN Targets t2 ON t2.id = Cases.target2
    LEFT JOIN 
    (SELECT case_id, avg(time) AS t FROM Times GROUP BY case_id) TbAvg
    ON Cases.id = TbAvg.case_id
    
    LEFT JOIN
    (SELECT case_id, count(time) AS n FROM Times GROUP BY case_id) TbCount
    ON Cases.id = TbCount.case_id
"""

# Formula:
# t: median solve time, d: days since last review, n: number of times
# priority =
#       t + t/(n+1) - t*( 1 - 1/(d+1) )
#
# Start with solve time,
# adjust slower based on low solve count,
# adjust faster based on long time since review
#
# Currently haven't implemented time since review yet.

order_cases = """
SELECT Cases.id, TbAvg.t, TbCount.n, t + (t / (n + 1)) as priority FROM Cases

INNER JOIN 
(SELECT case_id, avg(time) AS t FROM Times GROUP BY case_id) TbAvg
ON id = TbAvg.case_id

INNER JOIN
(SELECT case_id, count(time) AS n FROM Times GROUP BY case_id) TbCount
ON id = TbCount.case_id

WHERE Cases.type = ?
ORDER BY priority DESC
"""

cases_none = """
SELECT Cases.id from Cases

LEFT JOIN
(SELECT case_id, count(time) AS n FROM Times GROUP BY case_id) TbCount
ON id = TbCount.case_id

WHERE Cases.type = ? AND TbCount.n IS NULL
"""


@query
def all_cases(c, cat=1):
    c.execute(f"SELECT id FROM Cases WHERE type = ?", (cat,))
    return c.fetchall()


@query
def priority_cases(c, cat=1):
    c.execute(order_cases, (cat,))
    done = c.fetchall()
    c.execute(cases_none, (cat,))
    return c.fetchall() + done


@query
def next_case(c, cat=1):
    c.execute(order_cases, (cat,))
    done = c.fetchall()
    c.execute(cases_none, (cat,))
    undone = c.fetchall()
    if undone:
        return random.choice(undone)
    else:
        p = [r[3] for r in done]
        return random.choices(done, weights=p)


@query
def case_for_id(c, case_id):
    c.execute(f"{join_cases} WHERE Cases.id = ?", (case_id,))
    return c.fetchone()


@query
def submit(c, data):
    c.execute("INSERT INTO Times(time, date, case_id) VALUES (?,?,?);", data)


join_times = """
SELECT TOP 50 Times.id
    ,   Times.time
    ,   Times.date
    ,   t1.faces AS faces1
    ,   t2.faces AS faces2
    ,   t1.letter AS letter1
    ,   t2.letter AS letter2
FROM Times
    LEFT JOIN Cases ON Times.case_id = Cases.id
    LEFT JOIN Targets t1 ON t1.id = Cases.target1
    LEFT JOIN Targets t2 ON t2.id = Cases.target2
ORDER BY date DESC
"""


@query
def history(c):
    class Time:
        def __init__(self, data):
            self.id = data[0]
            self.time, self.date = data[1:3]
            self.case = f"UFR-{data[3]}-{data[4]} ({data[5]}{data[6]})"

    c.execute(join_times)
    return [Time(x) for x in c.fetchall()]


@query
def delete_time(c, tid):
    c.execute("DELETE FROM Times WHERE id = ?", (tid,))


@query
def stats(c, cat=1):
    c.execute("SELECT count(id) FROM Cases WHERE type=?", (cat,))
    total_cases = c.fetchall()[0][0]
    c.execute("SELECT count(id) FROM Cases WHERE id IN (SELECT case_id FROM Times)"
              " AND type=?", (cat,))
    done_cases = c.fetchall()[0][0]
    c.execute("SELECT count(time) FROM Times WHERE case_id IN"
              " (SELECT id FROM Cases WHERE type=?)", (cat,))
    time_count = c.fetchall()[0][0]
    c.execute("SELECT avg(time) FROM Times WHERE case_id IN"
              " (SELECT id FROM Cases WHERE type=?)", (cat,))
    time_avg = c.fetchall()[0][0]
    c.execute("SELECT avg(t) FROM (SELECT avg(time) AS t FROM Times GROUP BY case_id)")
    avg_avg = c.fetchall()[0][0]

    return total_cases, done_cases, time_count, round(time_avg, 3), round(avg_avg, 3)


case_stats = """
SELECT Cases.id, Cases.target1, Cases.target2, TbAvg.t, TbCount.n FROM Cases

INNER JOIN 
(SELECT case_id, avg(time) AS t FROM Times GROUP BY case_id) TbAvg
ON id = TbAvg.case_id

INNER JOIN
(SELECT case_id, count(time) AS n FROM Times GROUP BY case_id) TbCount
ON id = TbCount.case_id

WHERE Cases.type = ?
"""

case_max = """
SELECT min(TbAvg.t), max(TbAvg.t), max(TbCount.n) FROM Cases

INNER JOIN 
(SELECT case_id, avg(time) AS t FROM Times GROUP BY case_id) TbAvg
ON id = TbAvg.case_id

INNER JOIN
(SELECT case_id, count(time) AS n FROM Times GROUP BY case_id) TbCount
ON id = TbCount.case_id

WHERE Cases.type = ?
"""


@query
def time_grid(c, cat=1):
    grid = [[['', 'class=empty'] for _ in range(25)] for _ in range(25)]

    c.execute(case_max, (cat,))
    min_time, max_time, max_count = c.fetchall()[0]

    c.execute("SELECT target1, target2 FROM Cases WHERE Cases.type = ?", (cat,))
    for row in c.fetchall():
        grid[row[0]][row[1]] = ['-', 'class=notime']

    c.execute("SELECT id, faces, letter FROM Targets WHERE type = ?", (cat,))
    for row in c.fetchall():
        grid[0][row[0]] = [f"{row[1]} ({row[2]})", 'class=top']
        grid[row[0]][0] = [f"{row[1]} ({row[2]})", 'class=left']

    c.execute(case_stats, (cat,))
    for row in c.fetchall():
        hue = int(40 - 180 * (row[3] - min_time) / (max_time - min_time)) % 360
        sat = 100
        lum = int(20 + 20 * row[4] / max_count)
        grid[row[1]][row[2]] = [round(row[3], 2),
                                f'class=time style=background-color:hsl({hue},{sat}%,{lum}%);']

    return grid


if __name__ == '__main__':
    setup()
