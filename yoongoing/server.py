import pymysql
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

host = "http://localhost"
port = 8000

class my_handler(BaseHTTPRequestHandler):

    def _set_header(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()


    def _set_key_value(self, lists):
        set = {}

        for list in lists:
            temp = list.split('=')
            set[temp[0]] = temp[1]

        return set


    #create
    def do_POST(self):
        self._set_header()

        path = self.path
        if '?' in self.path:
            urls = self.path.split('?')
            request = urls[0]
            kv = urls[1].split('&')

        kv = self._set_key_value(kv)
        print(kv)


        if(request == '/create_docker'):
            res = requests.post(url=url, params=params)

            conn = pymysql.connect(host='localhost', user='root', password='root1234', charset='utf8')
            cursor = conn.cursor()

            sql = "insert into docker (ID,name,image,port,command,label_idx) values ({},{},{},{},{},{})"\
                .format(kv['ID'], kv['name'], kv['image'], kv['port'], kv['command'], kv['label_idx'])

            cursor.execute(sql)

            conn.commit()
            conn.close()



httpd = HTTPServer(('localhost', port), my_handler)
print('Server running on port : 8000')
httpd.serve_forever()