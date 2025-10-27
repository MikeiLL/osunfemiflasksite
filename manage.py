import psycopg2
import clize
import utils
import os
import json
from flask_login import UserMixin
from dataclasses import dataclass
from dotenv import load_dotenv
import stripe

from dotenv import load_dotenv

load_dotenv()
from database import query, dict_query

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]

_commands = []
def cmdline(f):
    _commands.append(f)
    return f

@dataclass
class User(UserMixin):
    id: int
    fullname: str
    ifaorishaname: str
    email: str
    user_level: int
    grade_level: int
    stripe_customer_id: str

    @classmethod
    def from_id(cls, id, password=None):
        data = query("SELECT " + ", ".join(cls.__dataclass_fields__) + " FROM users WHERE id=%s", (id,))
        if not len(data): return None
        user = data[0]
        if not user: return None
        return cls(*user)

    @classmethod
    def from_credentials(cls, login, password):
        data = query("SELECT " + ", ".join(cls.__dataclass_fields__) + ", password FROM users WHERE email=%s", (login.lower(),),)
        if not len(data): return None
        user = data[0]
        if not user: return None
        if not utils.check_password(password, user[-1]):
            # Passwords do not match. Pretend the user doesn't exist.
            # Note that even if the user _really_ doesn't exist, we still
            # do a password verification. This helps protect against
            # timing-based attacks.
            return None
        return cls(*user[:-1])


@cmdline
def create_user(fullname, email, password, ifaorishaname='', status=1):
    """Create a new user, return the newly-created ID

    username: Name for the new user

    email: Email address (must be unique)

    password: Clear-text password

    Optional: ifaorishaname, status
    """
    email = email.lower()
    stripename = "%s (%s)" % (fullname, ifaorishaname) if ifaorishaname else fullname
    try:
        stripe_customer = stripe.Customer.create(
                name=stripename,
                email=email,
        )
    except stripe.error.InvalidRequestError as e:
            return {'error':str(e)}
    pwd = utils.hash_password(password)
    try:
        info = query("""INSERT INTO users (fullname, email, password, ifaorishaname, stripe_customer_id, status, hex_key, grade_level)
              VALUES (%s, %s, %s, %s, %s, %s, %s, 0) RETURNING id, hex_key""", \
                                        (fullname, email, pwd, ifaorishaname, stripe_customer.id, status, utils.random_hex()))
        if isinstance(info[0], str):
            return {"error": info}
        return info[0]
    except (psycopg2.errors.NotNullViolation, psycopg2.errors.UniqueViolation, psycopg2.IntegrityError) as e:
        stripe.Customer.delete(stripe_customer.id)
        return {
            "error": "Wait a minute. You may already have an account under that name. \n This error occurred: \n" +str(e),
        }

@cmdline
def set_user_password(email, password):
    """Change a user's password (administratively) - returns None on success, or error message

    email: User email address

    password: New password
    """
    email = email.lower()
    pwd = utils.hash_password(password)
    rows=query("SELECT id FROM users WHERE email=%s", (email, ),)
    if not rows:
        print("No such user")
    else:
        query("update users set password=%s where id=%s", (pwd, rows[0][0]))

@cmdline
def delete_user(email, fullname):
    """
    Remove a user by identified by email and fullname
    """
    rows=query("DELETE FROM users WHERE email=%s and fullname = %s RETURNING id", (email, fullname,),)
    if not rows:
        return "No such user"
    else:
        print(rows[0])
        return "User Deleted"

@cmdline
def tables(*, confirm=False):
    """Update tables based on create_table.sql

    confirm: If omitted, will do a dry run.
    """
    tb = None; cols = {}; coldefs = []
    def finish():
        if tb and (coldefs or cols):
            if is_new == "": query_string = "create table "+tb+" ("+", ".join(coldefs)+")"
            else:
                parts = coldefs + ["drop "+c for c in cols]
                query_string = "alter table "+tb+" "+", ".join(parts)
            if confirm: query(query_string)
            else: print(query_string)

    for line in open("create_table.sql"):
        line = line.rstrip()
        if line == "" or line.startswith("--"): continue
        # Flush-left lines are table names
        if line == line.lstrip():
            finish()
            tb = line; coldefs = []
            rows = query("select column_name, data_type from information_schema.columns where table_name=%s", (tb,))
            cols = {row[0]:row[1] for row in rows}
            # New tables want a series of column definitions; altered tables want any added
            # columns prefixed with the command "add".
            is_new = "add" if cols else ""
            continue
        # Otherwise, it should be a column definition, starting (after whitespace) with the column name.
        colname, defn = line.strip().split(" ", 1)
        if colname in cols:
            # Column already exists. Check its data type.
            # Assume that all data types are unique within one space-delimited word. For example,
            # the data type "double precision" will be treated as "double".
            # NOTE: You may not be able to use this to change a data type to or from 'serial',
            # since that's not (strictly speaking) a data type.
            want_type = defn.split(" ", 1)[0]
            want_type = {
                "double": "double precision",
                "serial": "integer", "int": "integer",
                "varchar": "character varying",
                "timestamptz": "timestamp with time zone",
            }.get(want_type, want_type)
            have_type = cols[colname]
            if want_type != have_type:
                coldefs.append("alter %s set data type %s" % (colname, want_type))
            del cols[colname]
        else:
            # Column doesn't exist. Add it!
            # Note that we include a newline here so that a comment will be properly terminated.
            # If you look at the query, it'll have all its commas oddly placed, but that's okay.
            coldefs.append("%s %s %s\n" % (is_new, colname, defn))
    finish()
    if not confirm: print("Add --confirm to actually make the changes.")

if __name__ == "__main__":
    clize.run(*_commands, description="Commandline tools from admin.py")
