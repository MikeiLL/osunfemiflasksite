import psycopg2
import psycopg2.extras
import os


DATABASE_URL = os.environ["DATABASE_URL"]
_conn = psycopg2.connect((DATABASE_URL))

def dict_query(query, params=()):
  with _conn, _conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    cur.execute(query, params, )
    if not cur.description is None:
        return cur.fetchall()

def query(query, params=()):
  print(query, params)
  with _conn, _conn.cursor() as cur:
    cur.execute(query, params, )
    if not cur.description is None:
        return cur.fetchall()
