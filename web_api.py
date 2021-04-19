from http.server import HTTPServer, BaseHTTPRequestHandler
from os.path import abspath

CSV_DIR_PATH = abspath(".\\tmp\\separated csv\\")
TEST_HTTP = "http://127.0.0.1:5000/show?channel,country,sum-impressions_as_impressions,sum-clicks_as_clicks&date:2017-06-01&group:channel,country&order:clicks"


class ServiceHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text')
        get_request = self.requestline
        endpoint = get_request.split('/')[1].split(' ')[0]

        result = self.args_handler(endpoint)

        self.end_headers()
        self.wfile.write(bytes(f"{result}", 'utf-8'))
        return

    def args_handler(self, line_to_parse:str):
        result = ''
        print(line_to_parse)
        if line_to_parse == '':
            result = f"Hello, we have some products, check it out.\n(example {TEST_HTTP})"
        elif 'show' not in line_to_parse:
            result = f"There is only one endpoint, stick to it please.\n(example {TEST_HTTP})"
        elif '?' not in line_to_parse:
            result = "Please, choose some parameters"
        else:
            args = line_to_parse.split('?')[1].split('&')

            for arg in args:
                if "sku" in arg:
                    sku = arg.split('=')[1]
                elif "rank" in arg:
                    rank = arg.split('=')[1]
            if isinstance(sku, type(None)):
                result = "Sorry, but sku is obligatory, rank is optional"
        return result

    def shut_down(self):
        self.server.server_close()


def main():
    server = HTTPServer(('127.0.0.1', 5000), ServiceHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
