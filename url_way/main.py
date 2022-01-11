from http.server import HTTPServer, BaseHTTPRequestHandler
from base_handler import BaseHandler

TEST_HTTP = ''.join("""http://127.0.0.1:5000/expose_data?
                show:channel,country,sum_impressions_as_impressions,sum_clicks,
                cast_cpi=sum_spend//sum_installs
                &filter:date_>_"2017-06-01"_and_date_<_"2017-06-02"_or_country_=_"US"
                &group:channel,country
                &order:clicks-desc""".split())
DATABASE_NAME = 'adjust'
COLUMNS_OF_TABLE = ('all', 'id', 'date', 'channel', 'country', 'os',
                    'impressions', 'clicks', 'installs', 'spend', 'revenue')
OPERATORS = ('+', '-', '*', '//')


def parse_sum_in_select(select_part:str, as_part = True) -> str:
    column_name = select_part.split()[1]
    if column_name not in COLUMNS_OF_TABLE:
        raise KeyError(f"ERROR: {column_name} not in table")
    if not as_part:
        sql_part = f'SUM({column_name})'
        return sql_part
    if 'as' in select_part:
        new_name = select_part.split()[-1]
        if len(new_name) > 15: # not a valid 'as' name
            new_name = column_name
        sql_part = f'SUM({column_name}) as {new_name}'
    else:
        sql_part = f'SUM({column_name}) as {column_name}'
    return sql_part

def parse_arg_to_select_query(select_part:str) -> str:
    select_part = select_part.lower()
    if 'cast' in select_part:
        cast_name = select_part.split("cast")[1].strip().split('=')[0].strip()
        cast_body = select_part.split('=')[1].strip()
        
        for operator in OPERATORS:
            if operator in cast_body:
                cast_first_operand = cast_body.split(operator)[0].strip()
                cast_second_operand = cast_body.split(operator)[1].strip()
                if 'sum' in cast_first_operand or 'sum' in cast_second_operand:
                    cast_first_operand_sql = parse_sum_in_select(cast_first_operand, as_part=False)
                    cast_second_operand_sql = parse_sum_in_select(cast_second_operand, as_part=False)
                break
        else:
            raise ValueError("Operator for CAST operation is incorrect")
        sql_part = f'CAST({cast_first_operand_sql} {operator} {cast_second_operand_sql} as DECIMAL(10,4)) as {cast_name}'
    elif 'sum' in select_part:
        sql_part = parse_sum_in_select(select_part)
    else:
        if select_part not in COLUMNS_OF_TABLE:
            raise KeyError(f"ERROR: {select_part} not in table")
        sql_part = f'{select_part}'

    return sql_part


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
        elif 'expose_data' not in line_to_parse:
            result = f"There is only one endpoint, stick to it please.\n(example {TEST_HTTP})"
        elif '?' not in line_to_parse:
            result = "Please, choose some parameters"
        elif ';' in line_to_parse:
            result = "Symbol ';' is not allowed in query"
        else:
            args = line_to_parse.split('expose_data?')[-1].split('&')
            sql = self.convert_args_to_sql(args)

            args = 'select * from data;'
            df = self.convert_to_df(args)

            result = df.to_html()
        return result

    def convert_args_to_sql(self, args) -> str:
        sql = ''
        print(args)
        from_block = 'from data'

        for arg in args:
            if 'show' in arg:
                select_block = arg.split('show:')[1].replace('_', ' ')
            elif "filter" in arg:
                where_block = arg.split('filter:')[1].replace('_', ' ')
            elif "group" in arg:
                group_block = arg.split('group:')[1].replace('_', ' ')
            elif "order" in arg:
                order_block = arg.split('order:')[1].split('-')

        if select_block:
            print(select_block)
            sql_select_part = []
            for item in select_block.split(','):
                sql_part = parse_arg_to_select_query(item)
                sql_select_part.append(sql_part)

            select_block = ', '.join(sql_select_part)
            sql_select = f'select {select_block}'
        else:
            sql_select = 'select *'

        if where_block:
            sql_where = 'where ' + where_block.replace('"', "'")
        else:
            sql_where = ''

        if group_block:
            sql_group = 'group by ' + group_block.replace(',', ', ')

        if order_block:
            if order_block[-1] == 'desc' or order_block[-1] == 'asc':
                order = order_block[-1]
                order_block = order_block[:-1]
            else:
                order = 'desc'
            sql_order = 'order by ' + ', '.join(order_block) + ' ' + order

        sql = f'{sql_select}\n{from_block}\n{sql_where}\n{sql_group}\n{sql_order}'
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
    args = TEST_HTTP.split('expose_data?')[-1].split('&')
    # args = ['channel,country,sum-impressions_as_impressions,sum-clicks_as_clicks', 'where:date_>_2017-06-01', 'group:channel,country', 'sort:clicks','order:desc']
    sql = ServiceHandler.convert_args_to_sql(None,args)
    print(sql)


if __name__ == '__main__':
    test()
    # main()