from http.server import BaseHTTPRequestHandler, HTTPServer
#Used to create our own web servers. like how get, post and other methods should be handled.
import os

from urllib.parse import parse_qs, unquote, quote
#quote is to replace special characters with encoded code like space is converted to %20.
#unquote is to replace encoded code to normal code with special characters.
#parse_qs is used to extract parameters from the path.

memory = {}

#The below form is used when someone makes a get request that is when some access thr uri
#You can write your own html code here.Make sure to add {{ instead of { when using styles.
#One more curly braces is used to escape the curly brace. https://docs.python.org/3.4/library/string.html#format-string-syntax
form = '''<!DOCTYPE html>
<head>
    <title>Yashwanth URL Shortner</title>
    <style>
        input{{
      width:100%;
    }}
    body{{
        padding: 0 10px;
        height: 100vh;
        margin: 0;
        background-color: #02b3e4;
    }}
    header{{
        padding: 20px 0;
        text-align: center;
        font-variant: short-caps;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
        color: white;
    }}
    form{{
        background: rgba(152, 147, 147, 0.4);
        padding: 15px;
        border-radius: 5px;
        margin-bottom:10px;
    }}
    form input{{
        margin: 0;
        padding: 10px 0 10px 5px;
        border-radius: 5px;
        margin-bottom: 5px;
    }}
    #form_button{{
        padding: 10px;
    }}
    footer{{
        bottom: 0px;
        text-align: center;
        position: absolute;
    }}
    #url{{
        padding: 15px;
        border-radius: 5px;
        border: 1px dashed; 
        margin-bottom:5px;
    }}
    #url > a{{
        color:white;
        font-size:18px;
    }}
    #url:nth-child(odd){{
        border:1px dashed white;
        color:white;
    }}
    #url:nth-child(odd) > a {{
        color:black;
    }}
  </style>
</head>
<body>
    <header>Yashwanth URI Shortner</header>
    <form method="POST">
        <input type="url" name="originalurl" placeholder="Enter the url to be shortend">
        <input type="text" name='shorturl' placeholder="Name to be assigned to the url">
        <button id="form_button" type="submit">Short it!!</button>
    </form>
    {}
</body>
<footer>
    By Yashwanth Korla.
</footer>
</html>
'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self): # to handle get request
        url_path = unquote(self.path[1:]) # to unquote the query path.
        if url_path:
            if url_path in memory:
                # response from the server to the client.
                self.send_response(303) # redirect code
                self.send_header('Location',memory[url_path]) #when you access some shortend link i.e. localhost:8090/<short_url_name> It will
                #fetch the value from the memory and redirect to the original url.
                self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8') # telling the browser to use which parser when the response comes
            self.end_headers()
            saved_url = '\n'.join('<div id="url"><a href="/{}">{}</a> : {}</div>'.format(key,key,memory[key]) for key in sorted(memory.keys())) #saved links
            self.wfile.write(form.format(saved_url).encode()) #html response

    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode() # reading the query path
        params = parse_qs(body)
        if 'originalurl' not in params or 'shorturl' not in params:
            # code to handle missing fields.
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('Missing Some fields'.encode())
        else:
            orginal_uri = params['originalurl'][0]
            short = params['shorturl'][0]
            if short in memory:
                self.send_response(400)
                self.send_header('content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('The shorturl name is already taken'.encode())
            else:
                memory[short] = orginal_uri 
                # Instead of using local memoery you can connect to your db and save these in form of key value pair.So next time when a new users 
                # try to connect to the url, you can show up all the details.

                #Other usecase is , you can implement login feature so that only a particular user can see the details of the urls which he shortend.

                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()


if __name__ == '__main__':
    server = ('', 8090)
    http_server = HTTPServer(server, Handler)
    http_server.serve_forever()
