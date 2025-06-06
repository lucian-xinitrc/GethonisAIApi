from db import DBConnection

class Authentication():
	auth = False
	conn: str
	def __init__(self):
		session = DBConnection()
		self.conn = session.conn
	def check_auth(self, token):
		api_tokens = self.conn.cursor()
		api_tokens.execute(f"SELECT * FROM public.tokens WHERE token = '{token}'")
		if api_tokens.fetchone():
			self.auth = True