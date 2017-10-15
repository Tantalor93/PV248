import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.name = re.sub( '\([0-9+-]+\)', '', string)
        rx = re.compile(r".*\((....)-(....)\)")
        rx2 = re.compile(r".*\((....)--(....)\)")
        m = rx.match(string)
        m2 = rx2.match(string)
        if m is not None:
            self.born = m.group(1)
            self.died = m.group(2)
        else:
            if m2 is not None:
                self.born = m2.group(1)
                self.died = m2.group(2)
            else:
                self.born = None
                self.died = None


    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )
        self.id = self.cursor.fetchone()

    def do_store( self ):
        self.cursor.execute( "insert into person (name, born, died) values (?,?,?)", (self.name, self.born, self.died) )


class Score(DBItem):

    def __init__(self, conn, genre, key, incipit, year):
        super().__init__(conn)

        self.genre = genre
        self.key = key
        self.incipit = incipit
        self.year = year

    def fetch_id(self):
            self.cursor.execute( "select id from score where genre = ? AND key = ? AND incipit = ? AND year = ?", (self.genre, self.key, self.incipit, self.year) )
            self.id = self.cursor.fetchone()

    def do_store( self ):
        self.cursor.execute( "insert into score (genre, key, incipit, year) values (?,?,?,?)", (self.genre, self.key, self.incipit, self.year) )

class ScoreAuthor(DBItem):
    def __init__(self, conn, score, composer):
        super().__init__(conn)
        self.score = score.id[0]
        self.composer = composer.id[0]

    def fetch_id(self):
        self.cursor.execute( "select id from score_author where score = ? AND composer = ?", (self.score, self.composer) )
        self.id = self.cursor.fetchone()

    def do_store( self ):
        self.cursor.execute( "insert into score_author (score, composer) values (?,?)", (self.score, self.composer) )

conn = sqlite3.connect('scorelib.dat')
rx = re.compile(r"(.*): (.*)")

fileAsString = open('scorelib.txt', 'r', encoding='utf-8').read()
scores = fileAsString.split('\n\n')

for scoreString in scores:
    for line in scoreString.split('\n'):
        match = rx.match(line)
        if match is None: continue
        k = match.group(1)
        v = match.group(2)
        if k == 'Genre':
            genre = v
        if k == 'Key':
            key = v
        if k == 'Incipit':
            incipit = v
        if k == 'Composition Year':
            year = v
        if k == 'Composer':
            for c in v.split(';'):
                person = Person(conn, c.strip())
                person.store()

    score = Score(conn, genre, key, incipit, year)
    score.store()
    scoreAuthor = ScoreAuthor(conn, score, person)
    scoreAuthor.store()

conn.commit()
