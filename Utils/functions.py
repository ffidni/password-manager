popups = []

def goto_dashboard(dashboard, username, email, id):
	dashboard.account_widget.account_info.setText(f"Username: {username}\nEmail: {email}")
	dashboard.new_passwords(id)
	dashboard.goto_signal.emit("Dashboard")

def center_popup(popup, width, height, w_factor=None, h_factor=None):
	if w_factor and h_factor:
		pass
	else:
		popup.move((width//6)+10, (height//4)-20)
		
def shorten_text(name=None, email=None):
	email_len = len(email)
	if len(name) > 18:
		name = name[:-15] + ".."
	if email_len > 25:
		if email_len <= 28:
			email = email[:-10] + ".."
		else:
			email = email[:-12] + ".."
	return (name, email)