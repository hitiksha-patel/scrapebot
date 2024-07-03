from app import app

if __name__ == '__main__':
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8000, app)
    print('Serving on http://localhost:8000')
    httpd.serve_forever()
