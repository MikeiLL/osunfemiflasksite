import psycopg2
import os


DATABASE_URL = os.environ["DATABASE_URL"]
_conn = psycopg2.connect((DATABASE_URL))

def query(query, params=()):
  with _conn, _conn.cursor() as cur:
    cur.execute(query, params, )
    if not cur.description is None:
        return cur.fetchall()
