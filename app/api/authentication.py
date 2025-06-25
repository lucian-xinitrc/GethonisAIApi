from db import DBConnection

class Authentication():
	auth = False
	conn: str
	def __init__(self):
		session = DBConnection()
		self.conn = session.conn
	def check_auth(self, token):
		api_tokens = self.conn.cursor()
		api_tokens.execute("SELECT * FROM tokens WHERE token = %s", (token,))
		result = api_tokens.fetchone()

		if result:
			self.auth = True
			self.conn.commit()
		else:
			self.auth = False