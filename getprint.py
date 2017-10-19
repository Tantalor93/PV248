import sys
import sqlite3
import json

printNumber = sys.argv[1]

conn = sqlite3.connect('scorelib.dat')
cursor = conn.cursor()
result = cursor.execute("SELECT person.born, person.died, person.name, print.id "
                        "FROM person JOIN score_author ON person.id = score_author.composer "
                        "JOIN score ON score_author.score = score.id "
                        "JOIN edition ON score.id = edition.score "
                        "JOIN print ON edition.id = print.edition WHERE print.id = ?", (printNumber,)).fetchall()

list = list()

for composer in result:
    d = {"born": composer[0], "died": composer[1], "name": composer[2], "print": composer[3]}
    list.append(d)

print(json.dumps(list, indent=4))
