import sqlite3

class Database:

	def __init__(self, url):
		self.conn = sqlite3.connect(url)
		self.cursor = self.conn.cursor()
		try:
			with self.conn:
				self.cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
														username VARCHAR(30), email VARCHAR(320))""")
				self.cursor.execute("""CREATE TABLE apps (id INTEGER PRIMARY KEY AUTOINCREMENT,
														  name TEXT, icon_url TEXT)""")
				self.cursor.execute("""CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT,
														  	   user_id INTEGER, app_id INTEGER, username VARCHAR(50), password 
														  	   VARCHAR(256), is_hidden INTEGER DEFAULT 0)""")
				self.cursor.execute("""CREATE TABLE last_login (user_id INTEGER)""")
				self.cursor.execute("""CREATE TABLE hotkeys (id INTEGER PRIMARY KEY AUTOINCREMENT, hotkey VARCHAR(20))""")
		except Exception as existed:
			pass

	def remove_account(self, id):
		with self.conn:
			self.cursor.execute("DELETE FROM users WHERE id = ?", (id,))
			self.cursor.execute("DELETE FROM accounts WHERE user_id = ?", (id,))

	def set_last(self, user_id):
		with self.conn:
			self.cursor.execute("INSERT INTO last_login VALUES (user_id)")

	def remove_app(self, user_id, app_id):
		with self.conn:
			self.cursor.execute("UPDATE accounts SET is_hidden = 1 WHERE user_id = ? AND app_id = ?", (user_id, app_id))

	def register_user(self, username, email):
		with self.conn:
			data = self.is_exist("users", email)
			if data and email in data[0]:
				raise ValueError("User Already Exist")

			self.cursor.execute("INSERT INTO users(username, email) VALUES (?, ?)", (username, email))

	def update_hotkey(self, hotkey, id):
		with self.conn:
			self.cursor.execute("UPDATE hotkeys SET hotkey = ? WHERE id = ?", (hotkey, id))

	def register_hotkeys(self):
		defaults = ("<ctrl>+<shift>+g", "<ctrl>+<shift>+l", "<ctrl>+<shift>+s")
		for hk in defaults:
			with self.conn:
				self.cursor.execute("INSERT INTO hotkeys(hotkey) VALUES (?)", (hk,))

	def register_app(self, app_name, icon_url):
		with self.conn:
			self.cursor.execute("INSERT INTO apps(name, icon_url) VALUES (?, ?)", (app_name.lower(), icon_url))

	def register_app_account(self, user_id, app_id, username, password):
		with self.conn:
			self.cursor.execute("INSERT INTO accounts(user_id, app_id, username, password) VALUES (?, ?, ?, ?)", (user_id, app_id, username, password))


	def update_account(self, username, email, user_id):
		with self.conn:
			self.cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
			self.cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))


	def update_app_account(self, user_id, app_id, password, username=None):
		with self.conn:
			if username:
				self.cursor.execute("""UPDATE accounts SET username = ? WHERE user_id = ? AND app_id = ?""", (username, user_id, app_id))
			self.cursor.execute("""UPDATE accounts SET password = ? WHERE user_id = ? and app_id = ?""", (password, user_id, app_id))


	def is_exist(self, table, value):
		with self.conn:
			if table == 'users':
				self.cursor.execute("SELECT * FROM users WHERE email = ?", (value, ))
			else:
				self.cursor.execute("SELECT * FROM apps WHERE user_id = ?", (value, ))

		return self.cursor.fetchall()

	def get_hotkey(self, id):
		with self.conn:
			self.cursor.execute("SELECT hotkey FROM hotkeys WHERE id = ?", (id,))
		return self.cursor.fetchone()

	def get_icon(self, app_id):
		with self.conn:
			self.cursor.execute("SELECT icon_url FROM apps WHERE id = ?", (app_id,))
		return self.cursor.fetchone()

	def get_password(self, user_id, app_id):
		with self.conn:
			self.cursor.execute("SELECT password from accounts WHERE user_id = ? AND app_id = ?", (user_id, app_id))
		return self.cursor.fetchone()

	def get_id(self, email):
		with self.conn:
			self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
		return self.cursor.fetchone()

	def get_last_login(self):
		with self.conn:
			self.cursor.execute("SELECT user_id FROM last_login")

		data = self.cursor.fetchone()
		if not data:
			with self.conn:
				self.cursor.execute("INSERT INTO last_login VALUES (1)")
			return (1,)
		return data

	def set_last(self, user_id):
		with self.conn:
			self.cursor.execute("UPDATE last_login SET user_id =  ?", (user_id,))

	def get_app_name(self):
		with self.conn:
			self.cursor.execute("SELECT name FROM apps")
		return self.cursor.fetchall()

	def get_app(self, user_id=None, count=False):
		if user_id:
			with self.conn:
				if count:
					self.cursor.execute("""SELECT COUNT(accounts.app_id) FROM accounts 
									   	   JOIN apps ON apps.id = accounts.app_id AND accounts.user_id = ? AND accounts.is_hidden = 0""", (user_id,))
					return self.cursor.fetchone()
				else:
					self.cursor.execute("""SELECT apps.id, apps.name, accounts.is_hidden FROM accounts
										   JOIN apps ON apps.id = accounts.app_id AND accounts.user_id = ? """, (user_id,))
					return self.cursor.fetchall()
		else:
			with self.conn:
				self.cursor.execute("SELECT id, name FROM apps")
			return self.cursor.fetchall()

	def count_id(self, is_users=False):
		if is_users:
			with self.conn:
				self.cursor.execute("SELECT COUNT(id) FROM users")
			return self.cursor.fetchone()
		else:
			with self.conn:
				self.cursor.execute("SELECT COUNT(id) FROM apps")
			return self.cursor.fetchone()


	def get_app_id(self, app_name):
		with self.conn:
			self.cursor.execute("SELECT id FROM apps WHERE name = ?", (app_name,))
		return self.cursor.fetchone()

	def get_account(self, user_id):
		with self.conn:
			self.cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id, ))
		return self.cursor.fetchone()

	def get_app_account(self, user_id, app_id):
		with self.conn:
			self.cursor.execute("SELECT username, password, is_hidden FROM accounts WHERE user_id = ? AND app_id = ?", (user_id, app_id))
		return self.cursor.fetchone()

	def get_accounts(self, user_id):
		with self.conn:
			self.cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id, ))
		return self.cursor.fetchall()

	def get_users(self, user_id=False):
		if user_id:
			with self.conn:
				self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
			return self.cursor.fetchone()
		else:
			with self.conn:
				self.cursor.execute("SELECT * FROM users")
			return self.cursor.fetchall()

	def get_data(self, table):
		with self.conn:
			self.cursor.execute("SELECT * FROM '{}'".format(table))
			
		return self.cursor.fetchall()
