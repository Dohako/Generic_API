from d_utils import get_psql_env
from psycopg2 import connect


def main():
    database, user, password, host, port = get_psql_env()
    conn = connect(database='adjust', user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

def execute_sql(db_cursor, line):
    sql = 'select * from data;'
    db_cursor.execute(sql)
    first_level = db_cursor.fetchall()
    print(first_level[-1])


if __name__ == '__main__':
    main()