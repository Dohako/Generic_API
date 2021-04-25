from http.server import HTTPServer, BaseHTTPRequestHandler
from os.path import abspath
from base_handler import BaseHandler

CSV_DIR_PATH = abspath(".\\tmp\\separated csv\\")
TEST_HTTP = "http://127.0.0.1:5000/show?channel,country,sum-impressions_as_impressions,sum-clicks_as_clicks&where:date_2017-06-01&group:channel,country&order:clicks"

DATABASE_NAME = 'adjust'
TABLE_NAME = 'data'
COLUMNS_OF_TABLE = ['all', 'id', 'date', 'channel', 'country', 'os',
                    'impressions', 'clicks', 'installs', 'spend', 'revenue']
SQL_COMMANDS = ['select', 'from', 'where', 'group', 'order', 'sum', 'as']


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

    def args_handler(self, line_to_parse: str):
        # result = ''
        print(line_to_parse)
        if line_to_parse == '':
            result = f"Hello, we have some information, check it out.\n(example {TEST_HTTP})"
        elif 'show' not in line_to_parse:
            result = f"There is only one endpoint, stick to it please.\n(example {TEST_HTTP})"
        elif '?' not in line_to_parse:
            result = "Please, choose some parameters"
        else:
            args = line_to_parse.split('?')[1].split('&')

            # for arg in args:
            #     sql = arg
            sql = self.convert_args_to_sql(args)

            args = 'select * from data;'
            df = self.convert_to_df(args)

            result = df.to_html()
            # print(result)
            # result.set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'),('border-style','solid'),('border-width','1px')]}])
            # for arg in args:
            #     if "sku" in arg:
            #         sku = arg.split('=')[1]
            #     elif "rank" in arg:
            #         rank = arg.split('=')[1]
            # if isinstance(sku, type(None)):
            #     result = "Sorry, but sku is obligatory, rank is optional"
        return result

    def convert_args_to_sql(self, args) -> str:
        sql = ''
        print(args)
        select_block = args[0]
        from_block = 'from data'
        where_block = ''
        group_block = ''
        order_block = ''
        other_args = args[1:]
        for arg in other_args:
            if "where" in arg:
                where_block = arg
            elif "group" in arg:
                group_block = arg
            elif "order" in arg:
                order_block = arg
        select_part = []
        for item in select_block.split(','):
            if 'sum' in item:
                if 'as' in item:
                    check = item.split('-')[1].split('_')[0]
                    if check in COLUMNS_OF_TABLE:
                        new_name = item.split('-')[1].split('_')[-1]
                        if new_name > check and new_name > 15:
                            new_name = check
                        part = f'sum({check}) as {new_name}'
                        select_part.append(part)
            else:
                if item in COLUMNS_OF_TABLE:
                    part = f'{item}'
                    select_part.append(part)
        select_block = ''
        for part in select_part:
            select_block += f'{part}, '
        select_block = select_block[:-2]

        if where_block:
            NotImplemented

        print(f"select {select_block}")
        print(f"{from_block}")
        print(f"{where_block}")
        print(f"group {group_block}")
        print(f"order {order_block}")
        return sql

    def convert_to_sql(self, line):
        respond_from_db = base.get_data(line)
        return respond_from_db

    def convert_to_df(self, line):
        df_from_db = base.get_df_from_data(line)
        return df_from_db

    def shut_down(self):
        self.server.server_close()


def main():
    global base
    base = BaseHandler(DATABASE_NAME)

    server = HTTPServer(('127.0.0.1', 5000), ServiceHandler)
    server.serve_forever()


def test():
    args = ['channel,country,sum-impressions_as_impressions,sum-clicks_as_clicks', 'where:date_2017-06-01', 'group:channel,country', 'order:clicks']
    sql = ServiceHandler.convert_args_to_sql(None,args)
    print(sql)


if __name__ == '__main__':
    test()