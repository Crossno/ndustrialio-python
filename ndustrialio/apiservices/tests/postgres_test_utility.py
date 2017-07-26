import psycopg2
import os

class PostgresTestUtility:

    def __init__(self, database, user, password, host):
        self.postgres_con = psycopg2.connect(database=database,
                                       user=user,
                                       password=password,
                                       host=host)
        self.postgres_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def initializeTestData(self, setup_file=None):
        try:
            with self.postgres_con.cursor() as cur:
                cur.execute(self.fileRead(setup_file))
        except Exception as e:
            print 'Error: Could not insert test data'
            raise e

    def executeQuery(self, query):
        rows = []
        with self.postgres_con.cursor() as cur:
            cur.execute(query)
            try:
                rows = cur.fetchall()
            except Exception:
                pass
        return rows

    def fileRead(self, path):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, path)
        with open(file_path, 'r') as f:
            return f.read()

    def close_connection(self):
        print 'Closing postgres connection...'
        self.postgres_con.close()