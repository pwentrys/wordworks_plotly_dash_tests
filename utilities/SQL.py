from sqlalchemy import create_engine
import pandas as pd


class SQL:
    def __init__(self, string):
        if isinstance(string, type(None)):
            string = 'mysql+pymysql://gappi:92cf6cc2050f9830996b42433da09d03a4baa26e5524b3b8075c2f076451650a@192.168.1.172:3306/linguistics?charset=utf8'
        self.engine = create_engine(string)
        self.conn = self.engine.connect()

    def execute(self, query: str):
        if not self.conn.closed:
            return self.conn.execute(query)
        return False

    def close(self):
        if not self.conn.closed:
            self.conn.close()

    def execute_table_cols(self, table: str, cols: list):
        if not self.conn.closed:
            return pd.read_sql_table(table, con=self.conn, columns=cols)
        return False
