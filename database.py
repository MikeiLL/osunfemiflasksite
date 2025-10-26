import psycopg2
import psycopg2.extras
import os

import utils


DATABASE_URL = os.environ["DATABASE_URL"]
_conn = psycopg2.connect((DATABASE_URL))

def dict_query(query, params=()):
  with _conn, _conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    cur.execute(query, params, )
    if not cur.description is None:
        return cur.fetchall()

def query(query, params=()):
  with _conn, _conn.cursor() as cur:
    cur.execute(query, params, )
    if not cur.description is None:
        return cur.fetchall()


def create_user(username, email, password):
	"""Create a new user, return the newly-created ID

	username: Name for the new user

	email: Email address (must be unique)

	password: Clear-text password
	"""
	username = username.lower(); email = email.lower()
	if not isinstance(password, bytes): password=password.encode("utf-8")
	hex_key = utils.random_hex()
	with _conn, _conn.cursor() as cur:
		pwd = utils.hash_password(password)
		try:
			cur.execute("INSERT INTO users (username, email, password, hex_key) VALUES (%s, %s, %s, %s) RETURNING id, hex_key", \
											(username, email, pwd, hex_key))
			return cur.fetchone()
		except psycopg2.IntegrityError as e:
			return "That didn't work too well because: %s Maybe you already have an account or \
					someone else is using the name you requested."%e

def confirm_user(id, hex_key):
    """Attempt to confirm a user's email address

    id: Numeric user ID (not user name or email)

    hex_key: Matching key to the one stored, else the confirmation fails
    """
    with _conn, _conn.cursor() as cur:
        cur.execute("UPDATE users SET status = 1, hex_key = '' WHERE id = %s AND hex_key = %s RETURNING username, email", (id, hex_key))
        return cur.fetchone() or (None, '')
