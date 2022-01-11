from psycopg2 import connect
from d_utils import get_psql_env
from pandas import read_sql


class BaseHandler:
    def __init__(self, db):
        self.db = db
        _, self.user, self.password, self.host, self.port = get_psql_env()

    def get_data(self, command):
        conn = connect(database=self.db, user=self.user,
                       password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_df_from_data(self, command):
        conn = connect(database=self.db, user=self.user,
                       password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        result = read_sql(command, conn)
        conn.close()
        return result

    def set_data(self, command):
        conn = connect(database=self.db, user=self.user,
                       password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    base = BaseHandler('adjust')
    sql = 'select * from data;'
    df = base.get_df_from_data(sql)
    print(df)
    print(type(df))