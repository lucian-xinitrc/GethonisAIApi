import os, dotenv, psycopg2
from dotenv import load_dotenv

load_dotenv()

class DBConnection():
	conn: str
	def __init__(self):
		load_dotenv()
		self.conn = psycopg2.connect(database=os.getenv('DATABASENAME'), host=os.getenv('DATABASEHOST'), user=os.getenv('DATABASEUSER'), password=os.getenv('DATABASEPASSWORD'))
		"""
		self.conn = psycopg2.connect(database="neondb",
		                        host="ep-nameless-dust-abu1ap91-pooler.eu-west-2.aws.neon.tech",
		                        user="neondb_owner",
		                        password="npg_LD0xQJt7TycR")
		"""
	def check_conn(self):
		if (self.conn):
			return "The connection is established."
		return "There is some error."