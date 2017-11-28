from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3
import json


class Handler(BaseHTTPRequestHandler):

    def do_search(self, composer):
        conn = sqlite3.connect('scorelib.dat')
        cursor = conn.cursor()
        result = cursor.execute("SELECT person.name, score.name FROM person JOIN score_author on person.id = score_author.composer JOIN score on score_author.score = score.id WHERE person.name LIKE ? ", ("%" + composer + "%",)).fetchall()

        dict = {}
        for i in result:
            if i[0] not in dict:
                dict[i[0]] = list()
            dict[i[0]].append(i[1])
        return dict;

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/result':
            qs = parse_qs(parsed.query)
            searchTerm = qs['q'][0]
            format = qs['f'][0]
            result = self.do_search(searchTerm)
            if format == 'json':
                jsonResult = json.dumps(result)
                self.send_response(200)
                self.wfile.write(bytes(jsonResult, encoding="utf-8"))



def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()

