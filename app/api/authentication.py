from db import DBConnection

class Authentication():
	auth = False
	conn: str
	def __init__(self):
		session = DBConnection()
		self.conn = session.conn
	def check_auth(self, token):
		api_tokens = self.conn.cursor()
		api_tokens.execute("SELECT tries FROM tokens WHERE token = %s", (token,))
		result = api_tokens.fetchone()

		if result:
			if int(result[0]) <= 2:
				self.auth = True
				api_tokens.execute("UPDATE tokens SET tries = tries + 1 WHERE token = %s", (token,))
				self.conn.commit()
		else:
			self.auth = False