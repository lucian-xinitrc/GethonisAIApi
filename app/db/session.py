import os, dotenv, psycopg2
from dotenv import load_dotenv
load_dotenv()

class DBConnection():
	conn: str
	def __init__(self):
		load_dotenv()
		self.conn = psycopg2.connect(database=os.getenv('DATABASENAME'), host=os.getenv('DATABASEHOST'), user=os.getenv('DATABASEUSER'), password=os.getenv('DATABASEPASSWORD'))
	def check_conn(self):
		if (self.conn):
			return "The connection is established."
		return "There is some error."