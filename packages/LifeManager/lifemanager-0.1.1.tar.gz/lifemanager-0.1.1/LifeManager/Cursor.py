import os
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

from .logger_config import logger


class Cursor:
    def __init__(self, minconn=1, maxconn=10):

        load_dotenv()
        self._config = {
            "dbname": "workmanager",
            "user": os.environ["PGUSER"],
            "password": os.environ["PGPASSWORD"],
            "host": os.environ["PGHOST"],
            "port": os.environ["PGPORT"],
        }

        self._connection_pool = SimpleConnectionPool(
            minconn=minconn, maxconn=maxconn, **self._config
        )

    @contextmanager
    def _cursor(self):

        conn = self._connection_pool.getconn()
        cursor = conn.cursor()

        try:
            yield cursor
            conn.commit()

        except Exception as e:
            conn.rollback()
            logger.exception("In @contextmanager's Exception")
            raise e

        finally:
            cursor.close()
            self._connection_pool.putconn(conn)
