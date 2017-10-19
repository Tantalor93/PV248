import json
import sys
import sqlite3

composer = sys.argv[1]

conn = sqlite3.connect('scorelib.dat')
cursor = conn.cursor()
result = cursor.execute("SELECT person.name, score.name FROM person JOIN score_author on person.id = score_author.composer JOIN score on score_author.score = score.id WHERE person.name LIKE ? ", ("%" + composer + "%",)).fetchall()

dict = {}
for i in result:
    if i[0] not in dict:
        dict[i[0]] = list()
    dict[i[0]].append(i[1])

print(json.dumps(dict, indent=4))
