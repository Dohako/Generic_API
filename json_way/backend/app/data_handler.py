from app.base_handler import BaseHandler

COLUMNS_OF_TABLE = ('all', 'id', 'date', 'channel', 'country', 'os',
                    'impressions', 'clicks', 'installs', 'spend', 'revenue')
SQL_COMMANDS = ('select', 'from', 'where', 'group', 'order', 'sum', 'as')
SQL_UNIONS = ("and", "or")
OPERATORS = ('+', '-', '*', '/')


def handle_data(request: dict):
    sql = parse_json_to_sql(request)
    result = get_data_from_db(sql)
    return result

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

def parse_json_to_sql(json: dict) -> str:
    """
    ON ERROR calls KeyError and ValueError
    """
    from_block = "from data"

    for key in json.keys():
        if 'select' in key:
            select_block = json[key]
        elif "filter" in key:
            where_block = json[key]
        elif "group" in key:
            group_block = json[key]
        elif "order" in key:
            order_block = json[key]

    if select_block:
        sql_select_part = []
        for item in select_block:
            if ';' in item:
                raise ValueError("ERROR: symbol ';' in request")
            if 'CAST' in item:
                cast_name = item.split("CAST")[1].strip().split('=')[0].strip()
                cast_body = item.split('=')[1].strip()
                
                for operator in OPERATORS:
                    if operator in cast_body:
                        cast_first_operand = cast_body.split(operator)[0].strip()
                        cast_second_operand = cast_body.split(operator)[1].strip()
                        if 'SUM' in cast_first_operand or 'SUM' in cast_second_operand:
                            cast_first_operand_sql = parse_sum_in_select(cast_first_operand, as_part=False)
                            cast_second_operand_sql = parse_sum_in_select(cast_second_operand, as_part=False)
                        break
                else:
                    raise ValueError("Operator for CAST operation is incorrect")
                sql_part = f'CAST({cast_first_operand_sql} {operator} {cast_second_operand_sql} as DECIMAL(10,4)) as {cast_name}'
            elif 'SUM' in item:
                sql_part = parse_sum_in_select(item)
            else:
                if item not in COLUMNS_OF_TABLE:
                    raise KeyError(f"ERROR: {item} not in table")
                sql_part = f'{item}'
            sql_select_part.append(sql_part)

        select_block = ', '.join(sql_select_part)
        sql_select = f'select {select_block}'
    else:
        sql_select = 'select *'

    if where_block:
        sql_where = 'where ' + ' '.join(where_block)
    else:
        sql_where = ''

    if group_block:
        sql_group = 'group by ' + ', '.join(group_block)

    if order_block:
        if order_block[-1] == 'desc' or order_block[-1] == 'asc':
            order = order_block[-1]
            order_block = order_block[:-1]
        else:
            order = 'desc'
        sql_order = 'order by ' + ', '.join(order_block) + ' ' + order

    sql = f'{sql_select}\n{from_block}\n{sql_where}\n{sql_group}\n{sql_order}'
    return sql

def get_data_from_db(line):
    base = BaseHandler('adjust')
    respond_from_db = base.get_data(line)
    return respond_from_db

def get_df_from_db(line):
    base = BaseHandler('adjust')
    df_from_db = base.get_df_from_data(line)
    return df_from_db

if __name__ == "__main__":
    json = {
        "select": [
            "channel",
            "country",
            "SUM impressions as my_impressions",
            "SUM clicks",
            "CAST CPI = SUM spend / SUM installs"
        ],
        "filter": [
            "date > '2017-06-01'",
            "and date < '2017-06-02'",
            "or country = 'US'"
        ],
        "group by": [
            "channel",
            "country"
        ],
        "order by": [
            "clicks",
            "desc"
        ]
    }

    sql = parse_json_to_sql(json)
    print(sql)
    print(get_data_from_db(sql))
    print(type(get_df_from_db(sql)))
