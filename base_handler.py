from psycopg2 import connect
from d_utils import get_psql_env


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

    def set_data(self, command):
        conn = connect(database=self.db, user=self.user,
                       password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
        conn.close()
