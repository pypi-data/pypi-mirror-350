from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


class Server(ThreadingHTTPServer):
    def __init__(self, server_address, RequestHandler, args):
        super().__init__(server_address, RequestHandler)
        self.args = args


class Handler(SimpleHTTPRequestHandler):
    server_version = "HTTP/1.0"
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server, directory=server.args.output)


def serve(args):
    address = (args.host, args.port)
    print(f'Serving on http://{address[0]}:{address[1]}/ at {args.output}')
    httpd = Server(address, Handler, args)
    httpd.serve_forever()
