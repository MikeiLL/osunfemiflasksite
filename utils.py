import bcrypt
import binascii
import os

def hash_password(password):
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(15)).decode('utf-8')

def check_password(password, hashed):
	return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def random_hex():
	return binascii.b2a_hex(os.urandom(8)).decode("ascii")
