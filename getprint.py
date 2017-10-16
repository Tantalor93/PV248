import sys
import sqlite3
import json

printNumber = sys.argv[1]

conn = sqlite3.connect('scorelib.dat')
cursor = conn.cursor()
result = cursor.execute( "SELECT person.born, person.died, person.name, print.id "
                         "FROM person join score_author on person.id = score_author.composer "
                         "join score on score_author.score = score.id "
                         "join edition on score.id = edition.score "
                         "join print on edition.id = print.edition WHERE print.id = ?", (printNumber,)).fetchall()

list = list()

for composer in result:
    d = {}
    d["born"] = composer[0]
    d["died"] = composer[1]
    d["name"] = composer[2]
    d["print"] = composer[3]
    list.append(d)

print(json.dumps(list, indent=4))