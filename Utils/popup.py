from Utils.buttons import *
from Utils.database import *
from Utils.functions import *

class QListWidgetItem(QListWidgetItem):

	def __init__(self, widget=None):
		super().__init__()
		self.widget = widget
		self.widget.list_widget = self


class Popup(QMainWindow):
	
	def __init__(self, parent=None):
		global popups
		super().__init__(parent)
		self.parent = parent
		self.db = self.parent.db
		self.central_widget = QDialog()
		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
		self.setCentralWidget(self.central_widget)
		popups.append(self)

	def init_ui(self):
		self.widget_management()
		self.setup_stylesheet()
		self.layout_management()

	def widget_management(self):
		pass

	def setup_stylesheet(self):
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		self.setGraphicsEffect(shadow)

	def layout_management(self):
		pass

	def show(self):
		super().show()
		for widget in popups:
			if widget != self and not widget.isHidden():
				widget.hide()


class LengthInput(QSpinBox):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setValue(16)
		self.setFixedSize(61, 20)
		self.setStyleSheet("QSpinBox{background: lightgrey;}")


class GenerateResult(Popup):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.installEventFilter(self)
		self.resize(366, 346)
		self.init_ui()

	def widget_management(self):
		self.close_btn = CloseButton(icon="Utils/Assets/close.png", cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.title = QLabel("Secure Password:")
		self.password = QLineEdit("-")
		self.copy_btn = CopyButton(icon="Utils/Assets/copy.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.password, parent=self)
		self.length_text = QLabel("Length:")
		self.length_input = LengthInput()
		self.reload_btn = ReloadButton(icon="Utils/Assets/reload.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.password, length_field=self.length_input, parent=self)
		self.hor_line = QFrame()
		self.save_text = QLabel("Save to:")
		self.save_input = QComboBox()
		self.save_btn = QPushButton("Save", cursor=QCursor(Qt.PointingHandCursor))

		self.title.setFont(QFont("MS Shell DLG 2", 15))
		self.password.setFont(QFont("Bahnschrift Light", 12))
		self.password.setAlignment(Qt.AlignCenter)
		self.password.setReadOnly(True)
		self.password.setCursor(Qt.IBeamCursor)
		self.copy_btn.setToolTip("Copy the password")
		self.hor_line.setFrameShape(QFrame.HLine)
		self.hor_line.setFixedWidth(220)
		self.save_text.setFont(QFont("MS Shell Dlg 2", 12))
		self.save_input.setFixedSize(109, 20)
		self.add_save_items()
		self.save_btn.setFixedSize(50, 24)
		self.save_btn.clicked.connect(self.save_password)
		self.close_btn.setFixedSize(16, 16)
		self.close_btn.setIconSize(QSize(16, 16))

	def add_save_items(self):
		apps = self.db.get_app(self.parent.current_user_id)
		for app in apps:
			is_hidden = app[2]
			if not is_hidden:
				app_name = app[1].title()
				self.save_input.addItem(app_name)

	def update_app_items(self):
		self.save_input.clear()
		self.add_save_items()

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.close_layout = QHBoxLayout()
		self.password_widget = QWidget()
		self.password_vlayout = QVBoxLayout()
		self.password_hlayout = QHBoxLayout()
		self.length_layout = QHBoxLayout()
		self.save_layout = QHBoxLayout()

		self.close_layout.addWidget(self.close_btn, alignment=Qt.AlignBottom | Qt.AlignRight)
		self.close_layout.addSpacing(20)
		self.main_layout.addSpacing(45)
		self.main_layout.addLayout(self.close_layout)
		self.main_layout.addSpacing(30)
		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		self.password_hlayout.addSpacing(10)
		self.password_hlayout.addWidget(self.password, alignment=Qt.AlignRight)
		self.password_hlayout.addWidget(self.reload_btn, alignment=Qt.AlignCenter)
		self.password_hlayout.addWidget(self.copy_btn, alignment=Qt.AlignLeft)
		self.password_vlayout.addLayout(self.password_hlayout)
		self.password_widget.setLayout(self.password_vlayout)
		self.main_layout.addWidget(self.password_widget, alignment=Qt.AlignCenter | Qt.AlignTop)
		self.length_layout.addWidget(self.length_text, alignment=Qt.AlignRight)
		self.length_layout.addWidget(self.length_input, alignment=Qt.AlignLeft)
		self.main_layout.addLayout(self.length_layout)
		self.main_layout.addWidget(self.hor_line, alignment=Qt.AlignCenter)
		self.save_layout.addSpacing(30)
		self.save_layout.addWidget(self.save_text, alignment=Qt.AlignRight)
		self.save_layout.addWidget(self.save_input, alignment=Qt.AlignCenter)
		self.save_layout.addWidget(self.save_btn, alignment=Qt.AlignLeft)
		self.main_layout.addLayout(self.save_layout)
		self.main_layout.addSpacing(25)
		self.central_widget.setLayout(self.main_layout)

	def setup_stylesheet(self):
		super().setup_stylesheet()
		self.save_btn.setStyleSheet("""background: #e0e0e0;
										 color: black;
										 border-radius: 8px;
										 border: 1px solid #424242;""")
		self.hor_line.setStyleSheet("color: #e0e0e0;")
		self.setStyleSheet("""QMainWindow{
				                     background-color: transparent;
								     border-image: url('Utils/Assets/lock_background.png');
								  }
								  QPushButton{
								  	color: #e0e0e0;
								  	background: transparent;
								  	border: none;
								  }
								  QLabel{
								  	color: #e0e0e0;
								  }
								  QLineEdit{
								  	color: #e0e0e0;
								  	background: transparent;
								  	border: 1px solid gray;
								  }""")

	def save_password(self):
		self.hide()
		app_name = self.save_input.currentText()
		user_id = self.parent.current_user_id
		app_id = self.db.get_app_id(app_name.lower())[0]
		app_widget = self.parent.parent.m_pages["Dashboard"].password_list.main_layout.itemAt(app_id+1).widget()
		password = self.password.text()
		self.db.update_app_account(user_id, app_id, password)
		self.parent.goto_signal.emit("Dashboard")
		app_widget.app_button.clicked.emit()
		app_widget.password_info.password_input.setText(password)
		app_widget.password_info.save_btn.setText("Saved")

	def eventFilter(self, obj, event):
		if event.type() == QEvent.MouseButtonPress:
			self.password.deselect()

		return super().eventFilter(obj, event)


class AccountInfo(QFrame):

	def __init__(self, shorten_info, unshorten_info, user_id, parent=None):
		super().__init__()
		self.shorten_info = shorten_info
		self.unshorten_info = unshorten_info
		self.account_info = QLabel(self.unshorten_info)
		self.list_widget = None
		self.user_id = user_id
		self.parent = parent
		self.main_layout = QHBoxLayout()
		self.icon = QPushButton(icon=QIcon("Utils/Assets/user.png"))
		self.edit_btn = EditButton(icon="", cursor=QCursor(Qt.PointingHandCursor), widget=self, parent=self.parent)
		self.delete_btn = DeleteButton(icon="", cursor=QCursor(Qt.PointingHandCursor), widget=self, user_id=self.user_id, parent=self.parent)

		self.setStyleSheet("""QFrame{
							    background: transparent;
							  }""")
		self.installEventFilter(self)
		self.icon.setIconSize(QSize(16, 16))
		self.icon.setFixedSize(16, 16)
		self.icon.setStyleSheet("background: transparent;")
		self.edit_btn.setFixedSize(1, 1)
		self.edit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.edit_btn.setIconSize(QSize(22, 22))
		self.edit_btn.clicked.connect(self.edit_account)
		self.edit_btn.installEventFilter(self)
		self.delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.delete_btn.setIconSize(QSize(14, 14))
		self.delete_btn.setFixedSize(1, 1)
		self.delete_btn.installEventFilter(self)
		self.account_info.setFixedWidth(180)
		self.main_layout.addWidget(self.icon, alignment=Qt.AlignRight)
		self.main_layout.addWidget(self.account_info, alignment=Qt.AlignCenter)
		self.main_layout.addWidget(self.edit_btn, alignment=Qt.AlignLeft)
		self.main_layout.addWidget(self.delete_btn, alignment=Qt.AlignLeft)
		self.setLayout(self.main_layout)

	def edit_account(self):
		dashboard = self.parent.parent
		account_info = self.unshorten_info.split()
		dashboard.account_edit.user_id = dashboard.db.get_id(account_info[1])[0]
		dashboard.account_edit.username_input.setText(account_info[0])
		dashboard.account_edit.email_input.setText(account_info[1])
		dashboard.account_edit.list_item = self
		dashboard.account_edit.show()

	def eventFilter(self, obj, event):
		if event.type() == QEvent.MouseButtonDblClick:
			self.parent.switch_account(self.list_widget)
		elif event.type() == QEvent.MouseButtonPress:
			if obj in (self.edit_btn, self.delete_btn):
				#if self.user_id == self.parent.parent.current_user_id:
				self.parent.list.setCurrentItem(self.list_widget)
		elif event.type() == QEvent.Enter:
			self.account_info.setText(self.shorten_info)
			self.edit_btn.setIcon(QIcon("Utils/Assets/white_pencil.png"))
			self.edit_btn.setFixedSize(22, 22)
			self.delete_btn.setIcon(QIcon("Utils/Assets/delete.png"))
			self.delete_btn.setFixedSize(22,22)
		elif event.type() == QEvent.Leave:
			self.account_info.setText(self.unshorten_info)
			self.edit_btn.setIcon(QIcon(""))
			self.edit_btn.setFixedSize(1, 1)
			self.delete_btn.setIcon(QIcon(""))
			self.delete_btn.setFixedSize(1, 1)

		return super().eventFilter(obj, event)


class SwitchAccount(Popup):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.setObjectName("Switch")
		self.resize(385, 370)
		self.init_ui()
		self.set_current()

	def widget_management(self):
		self.close_btn = CloseButton(icon="Utils/Assets/close.png", cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.title = QLabel("Account List")
		self.scrollarea = QScrollArea()
		self.list = QListWidget()
		self.add_btn = AddButton(icon=QIcon("Utils/Assets/new.png"), cursor=QCursor(Qt.PointingHandCursor), parent=self)

		self.load_accounts()
		self.title.setFont(QFont("MS SHell Dlg 2", 18))
		self.scrollarea.setWidget(self.list)
		self.list.setFixedSize(235, 140)
		self.list.horizontalScrollBar().setFixedHeight(100)
		self.list.setFont(QFont("Arial", 13))
		self.add_btn.clicked.connect(self.add_new)
		self.add_btn.setFixedSize(28, 28)
		self.add_btn.setIconSize(QSize(28, 28))

	def load_accounts(self):
		self.accounts = self.db.get_users()
		for info in self.accounts:
			name = info[1]
			email = info[2]
			shorten = shorten_text(name, email)
			shorten_name, shorten_email = shorten[0], shorten[1]
			shorten_info = f"{shorten_name}\n{shorten_email}"
			unshorten_info =  f"{name}\n{email}"
			user_id = self.db.get_id(email)[0]
			widget = AccountInfo(shorten_info, unshorten_info, user_id, self)
			list_widget = QListWidgetItem(widget=widget)
			widget.delete_btn.list_widget = list_widget
			self.list.insertItem(self.list.count(), list_widget)
			self.list.setItemWidget(list_widget, widget)
			list_widget.setSizeHint(QSize(180, 44))

	def add_new(self):
		self.hide()
		self.create_account = CreateAccount(self.parent, add_account=True)
		self.create_account.show()
		center_popup(self.create_account, self.parent.width(), self.parent.height())

	def set_current(self):
		current_user_id = self.db.get_last_login()[0]
		for index in range(self.list.count()):
			item = self.list.item(index)
			if item.widget.user_id == current_user_id:
				self.list.setCurrentItem(item)

	def switch_account(self, item):
		self.hide()
		info = item.widget.unshorten_info.split("\n")
		if info[0] != self.parent.account_widget.account_info.text()[10:15]:
			username = info[0]
			email = info[1]
			user_id = item.widget.user_id
			menu = self.parent.parent.m_pages["Menu"]
			dashboard = self.parent.parent.m_pages["Dashboard"]
			self.db.set_last(user_id)
			menu.current_user_id = user_id
			menu.generate_popup.update_app_items()
			dashboard.current_user_id = user_id
			goto_dashboard(self.parent.parent.m_pages["Dashboard"], username, email, user_id)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.close_layout = QHBoxLayout()

		self.close_layout.addWidget(self.close_btn, alignment=Qt.AlignRight | Qt.AlignBottom)
		self.close_layout.addSpacing(20)
		self.main_layout.addSpacing(50)
		self.main_layout.addLayout(self.close_layout)
		self.main_layout.addSpacing(40)
		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.main_layout.addSpacing(10)
		self.main_layout.addWidget(self.scrollarea, alignment=Qt.AlignCenter)
		self.main_layout.addWidget(self.add_btn, alignment=Qt.AlignCenter)
		self.main_layout.addSpacing(8)
		self.central_widget.setLayout(self.main_layout)

	def setup_stylesheet(self):
		super().setup_stylesheet()
		self.setStyleSheet("""QMainWindow{
			                     background-color: transparent;
							     border-image: url('Utils/Assets/key_background.png');
							}
							QPushButton{
								color: #e0e0e0;
								background: transparent;
								border: none;
							}
							QLabel{
								color: #e0e0e0;
							}
							QListWidget{
								color: #e0e0e0;
								background: #5a5959;
								border: 1px solid #424242;
							}
							QScrollArea{
								border: none;
							}""")


class Error(QMessageBox):

	def __init__(self, text="Error Message"):
		super().__init__()
		self.setWindowTitle("Error")
		self.setText(text)
		self.setIcon(QMessageBox.Critical)
		self.setStandardButtons(QMessageBox.Ok)
		self.buttonClicked.connect(self.hide)

class HotkeyPopup(QMessageBox):

	def __init__(self, parent, short_name=None, widget_input=None):
		super().__init__()
		self.parent = parent
		self.id = None
		self.short_name = short_name
		self.widget_input = widget_input
		self.db = Database("Utils/data.db")
		self.thread = HotkeyInputThread(self)
		self.thread.finished_signal.connect(self.finished_slot)
		self.thread.text_signal.connect(self.setInformativeText)
		self.setWindowTitle("HotKey Input")
		self.setText("Press Ctrl / Shift / Alt at the beginning\nand characters for the rest.")
		self.setIcon(QMessageBox.Information)
		self.buttonClicked.connect(self.ok_clicked)
		self.error = Error("HotKey combination is invalid!\nEvery combination must starts with Ctrl / Alt / Shift")
		self.error.buttonClicked.connect(self.reset_input)
		self.error.hide()

	def closeEvent(self, event):
		self.thread.terminate()

	def apply_input(self, keys):
		result_text = '+'.join(keys).title()
		result_keys = '+'.join(hk if hk.isalpha() and len(hk) == 1 else f"<{hk}>" for hk in keys) 
		self.hide()
		self.widget_input.setText(result_text)
		self.db.update_hotkey(result_keys, self.id)
		self.parent.hotkey_thread.hotkeys = self.parent.get_hotkeys()
		self.parent.hotkey_thread.terminate()
		self.parent.hotkey_thread.start()

	def closeEvent(self, event=None):
		super().closeEvent(event)
		self.reset_input()

	def ok_clicked(self, button):
		self.thread.terminate()
		self.thread.listener.stop()
		if len(self.thread.keys) > 1:
			self.thread.finished_signal.emit(self.thread.keys)
		else:
			self.hide()
			self.error.show()
		self.reset_input()

	@pyqtSlot(list)
	def finished_slot(self, keys):
		if keys:
			self.apply_input(keys)
		else:
			self.hide()
			self.error.show()
		self.reset_input()
		self.parent.hotkey_thread.start()

	def reset_input(self):
		self.setInformativeText("")
		self.thread.keys.clear()

	def show(self, short_name=None, widget=None):
		super().show()
		id = {"gen":1, "list":2, "switch":3}[short_name]
		if short_name and widget:
			self.short_name = short_name
			self.widget_input = widget
			self.id = id
		self.parent.hotkey_thread.stop()
		QTimer.singleShot(100, self.thread.start)


class HotkeyInputThread(QThread):
	finished_signal = pyqtSignal(list)
	text_signal = pyqtSignal(str)

	def __init__(self, popup):
		super().__init__()
		self.popup = popup
		self.keys = []
		self.allowed_chars = {"Key.ctrl_l":"Ctrl", "Key.alt_l":"Alt", "Key.shift":"Shift"}

	def on_press(self, key):
		approved_key = None
		try:
			if key.char.isalpha():
				approved_key = key.char
			if not len(self.keys):
				return False
		except:
			key = str(key)
			if key in self.allowed_chars:
				approved_key = self.allowed_chars[key]

		if approved_key and approved_key not in self.keys:
			self.keys.append(approved_key)
			self.text_signal.emit(f"Key combination: {'+'.join(self.keys)}")

		if len(self.keys) == 3:
			self.finished_signal.emit(self.keys)
			self.keys.clear()
			self.terminate()
			return False

	def run(self):
		with Listener(
			on_press=self.on_press) as self.listener:
			self.listener.join()
			self.finished_signal.emit([])


class CreateAccount(Popup):

	def __init__(self, parent=None, add_account=False, first=False, is_edit=False):
		super().__init__(parent)
		self.add_account = add_account
		self.first = first
		self.parent = parent
		self.is_edit = is_edit
		self.user_id = None
		self.list_item = None
		self.resize(385, 370)
		self.init_ui()
		self.hide()

	def widget_management(self):
		self.account_info = None
		self.error = Error()
		self.close_btn = CloseButton(icon="Utils/Assets/close.png", cursor=Qt.PointingHandCursor, parent=self)
		self.title = QLabel("Edit account" if self.is_edit else "Create an Account")
		self.username = QLabel("Username:")
		self.username_input = QLineEdit()
		self.email = QLabel("Email:")
		self.email_input = QLineEdit()
		self.submit_btn = QPushButton("Save" if self.is_edit else "Submit", cursor=QCursor(Qt.PointingHandCursor))
		self.copy_btn = CopyButton(icon="Utils/Assets/copy.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.username_input, parent=self)
		self.copy_btn_2 = CopyButton(icon="Utils/Assets/copy.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.email_input, parent=self)

		self.error.hide()
		self.title.setFont(QFont("MS Shell Dlg 2", 19))
		self.username.setFont(QFont("Bahnschrift Light", 14))
		self.username_input.setFixedSize(170, 23)
		self.username_input.setFont(QFont("Arial", 11))
		self.email.setFont(QFont("Bahnschrift Light", 14))
		self.email_input.setFixedSize(170, 23)
		self.email_input.setFont(QFont("Arial", 10))
		self.copy_btn.setToolTip("Copy the username")
		self.copy_btn_2.setToolTip("Copy the email")
		self.submit_btn.setFixedSize(80, 28)
		self.submit_btn.clicked.connect(self.save_account if self.is_edit else self.register)
		if self.is_edit:
			data = self.db.get_account(self.parent.current_user_id)
			if data:
				self.username_input.setText(data[0])
				self.email_input.setText(data[1])
				self.username_input.textChanged.connect(self.on_changed)
				self.email_input.textChanged.connect(self.on_changed)

	def on_changed(self, new):
		if self.submit_btn.text() == 'Saved': 
			self.submit_btn.setText("Save")

	def update_item(self, username, email):
		self.list_item.shorten_info = '\n'.join(shorten_text(username, email))
		self.list_item.unshorten_info = f"{username}\n{email}"
		self.list_item.account_info.setText(self.list_item.unshorten_info)

	def save_account(self):
		if self.submit_btn.text() != "Saved":
			username = self.username_input.text()
			email  = self.email_input.text()
			account_info = f"Username: {username}\nEmail: {email}"
			self.db.update_account(username, email, self.user_id)
			if self.list_item:
				self.update_item(username, email)
				if self.user_id == self.parent.current_user_id:
					self.parent.account_widget.account_info.setText(account_info)
			else:
				lw = self.parent.account_list.list
				for index in range(lw.count()):
					list_item = lw.item(index).widget
					if list_item.account_info.text() == self.account_info:
						self.list_item = list_item
						self.update_item(username, email)
				self.list_item = None
				self.parent.account_widget.account_info.setText(account_info)
			self.parent.username = username
			self.parent.email = email
			self.hide()

	def register(self):
		username = self.username_input.text().replace(" ", "")
		email  = self.email_input.text()
		if username and email:
			try:
				menu = self.parent.parent.m_pages["Menu"]
				dashboard = self.parent.parent.m_pages["Dashboard"]
				self.hide()
				self.parent.db.register_user(username, email)
				user_id = self.parent.db.get_id(email)[0]
				self.register_app(user_id, username, "")
				self.parent.db.set_last(user_id)
				menu.current_user_id = user_id
				dashboard.current_user_id = user_id
				menu.generate_popup.update_app_items()
				goto_dashboard(dashboard, username, email, user_id)
				menu.user_exist = True
				menu.parent.user_exist = True
				QTimer.singleShot(500, lambda: dashboard.account_list.list.setCurrentRow(dashboard.account_list.list.count()-1))
				if self.add_account:
					shorten = shorten_text(username, email)
					shorten_username, shorten_email = shorten[0], shorten[1]
					shorten_info = f"{shorten_username}\n{shorten_email}"
					unshorten_info = f"{username}\n{email}"
					user_id = self.parent.db.get_id(email)[0]
					account_widget = AccountInfo(shorten_info, unshorten_info, user_id, self.parent.account_list)
					list_widget = QListWidgetItem(widget=account_widget)
					account_widget.delete_btn.list_widget = list_widget
					dashboard.account_list.list.insertItem(dashboard.account_list.list.count(), list_widget)
					dashboard.account_list.list.setItemWidget(list_widget, account_widget)
					list_widget.setSizeHint(QSize(180, 44))
				elif self.first:
					dashboard.account_list.load_accounts()
			except ValueError as err:
				self.error.setText("User is already exists!")
				self.error.show()
		else:
			self.error.setText("Invalid Input!")
			self.error.show()

	def register_app(self, user_id, username, password):
		for app_id, app_name in enumerate(('instagram', 'telegram', 'whatsapp', 'facebook', 'google', 'twitter')):
			if user_id == 1:
				self.parent.db.register_app(app_name, "Utils/Assets/{}.png".format(app_name))
			self.parent.db.register_app_account(user_id, app_id+1, username, password)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.close_layout = QHBoxLayout()
		self.main_form = QHBoxLayout()
		self.form_layout = QFormLayout()
		self.field_layout = QHBoxLayout()
		self.field_layout_2 = QHBoxLayout()
		self.spacer = QLabel()
		self.spacer_2 = QLabel()

		self.close_layout.addWidget(self.close_btn, alignment=Qt.AlignBottom | Qt.AlignRight)
		self.close_layout.addSpacing(20)
		self.main_layout.addSpacing(40)
		self.main_layout.addLayout(self.close_layout)
		self.main_layout.addSpacing(40)
		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		self.main_layout.addSpacing(15)
		self.field_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
		self.field_layout.addWidget(self.copy_btn, alignment=Qt.AlignLeft)
		self.field_layout_2.addWidget(self.email_input, alignment=Qt.AlignCenter)
		self.field_layout_2.addWidget(self.copy_btn_2, alignment=Qt.AlignLeft)
		self.form_layout.addRow(self.username, self.field_layout)
		self.form_layout.addRow(self.spacer, self.spacer_2)
		self.spacer.setFixedSize(10, 2)
		self.spacer_2.setFixedSize(10, 2)
		self.form_layout.addRow(self.email, self.field_layout_2)
		self.form_layout.setSpacing(8)
		self.main_form.addSpacing(25)
		self.main_form.addLayout(self.form_layout)
		self.main_layout.addLayout(self.main_form)
		self.main_layout.addSpacing(15)
		self.main_layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)
		self.main_layout.addSpacing(10)
		self.central_widget.setLayout(self.main_layout)

	def setup_stylesheet(self):
		super().setup_stylesheet()
		self.submit_btn.setStyleSheet("""background: #e0e0e0;
										 color: black;
										 border-radius: 8px;
										 border: 1px solid #424242;""")
		self.setStyleSheet("""QMainWindow{
			                     background-color: transparent;
							     border-image: url('Utils/Assets/key_background.png');
							}
							QPushButton{
								color: #e0e0e0;
								background: transparent;
								border: none;
							}
							QLabel{
								color: #e0e0e0;
							}
							QLineEdit{
								color: #e0e0e0;
								background: #5a5a5a;
								border: 1px solid gray;
							}""")


class AppPass(Popup):

	def __init__(self, user_id, app_id, app_name, mparent=None, parent=None, icon_url=None, is_new=False):
		super().__init__(mparent)
		self.user_id = user_id
		self.app_id = app_id
		self.app_name = app_name
		self.parent = parent
		self.mparent = mparent
		self.old_user = None 
		self.old_pass = None
		self.icon_url = icon_url
		self.is_new = is_new
		self.setObjectName("AppPass")
		self.installEventFilter(self)
		self.resize(385, 370)
		self.init_ui()

	def widget_management(self):
		self.error = Error()
		self.close_btn = CloseButton(icon="Utils/Assets/close.png", cursor=QCursor(Qt.PointingHandCursor), parent=self)
		if not self.icon_url:
			self.icon_url = self.db.get_icon(self.app_id)[0]
		self.app_icon = AppButton(icon=self.icon_url, cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.app_title = QLineEdit(self.app_name.title())
		self.username = QLabel("Username:")
		self.username_input = QLineEdit()
		self.password = QLabel("Password:")
		self.password_input = QLineEdit()
		self.length_text = QLabel("Length:")
		self.length_input = LengthInput()
		self.reload_btn = ReloadButton(icon="Utils/Assets/reload.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.password_input, length_field=self.length_input, is_adapt=False, parent=self)
		self.copy_btn = CopyButton(icon="Utils/Assets/copy.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.username_input, parent=self)
		self.copy_btn_2 = CopyButton(icon="Utils/Assets/copy.png", cursor=QCursor(Qt.PointingHandCursor), input_field=self.password_input, parent=self)
		self.toggle_password = TogglePassword(icon="Utils/Assets/hide_password.png", cursor=QCursor(Qt.PointingHandCursor), parent=self) 
		self.save_btn = QPushButton("Save", cursor=QCursor(Qt.PointingHandCursor))

		self.close_btn.clicked.connect(self.hide_widget)
		self.app_icon.setToolTip("Change icon")
		self.app_title.setFont(QFont("MS Shell Dlg 2", 19))
		self.app_title.setAlignment(Qt.AlignCenter)
		self.app_title.setReadOnly(True)
		self.app_title.setCursor(QCursor(Qt.PointingHandCursor))
		self.app_title.installEventFilter(self)
		self.app_title.setMaxLength(20)
		self.app_title.textChanged.connect(lambda value: self.value_changed(value, self.app_title))
		self.app_title.returnPressed.connect(self.unfocus_input)
		self.adapt_size()
		self.username.setFont(QFont("Bahnschrift Light", 14))
		self.username_input.setFixedSize(170, 23)
		self.username_input.textChanged.connect(self.value_changed)
		self.username_input.setFont(QFont("Arial", 11))
		self.password.setFont(QFont("Bahnschrift Light", 14))
		self.password_input.setFixedSize(170, 23)
		self.password_input.setFont(QFont("Arial", 10))
		self.password_input.textChanged.connect(self.value_changed)
		self.copy_btn.setToolTip("Copy the username")
		self.copy_btn_2.setToolTip("Copy the password")
		self.reload_btn.setToolTip("Generate new password")
		self.save_btn.setFixedSize(80, 28)
		self.save_btn.clicked.connect(self.save_info)

	def hide_widget(self):
		if self.save_btn.text() != 'Saved':
			self.app_icon.current_img = self.app_icon.old_img
			self.app_icon.setIcon(QIcon(self.app_icon.current_img))
			self.app_title.setText(self.app_name.capitalize())
			self.username_input.setText(self.old_user)
			self.password_input.setText(self.old_pass)
		if self.is_new:
			password_list = self.parent.parent.password_list
			app_id = self.parent.app_id+1
			widget = password_list.main_layout.itemAt(app_id).widget()
			password_list.main_layout.removeWidget(widget)
			widget.deleteLater()
		if not self.length_input.isHidden():
			self.reload_btn.hide_length()

		self.mparent.password_list.current_opened = None
		self.hide()

	def unfocus_input(self):
		self.app_title.setFocus(False)
		self.app_title.setReadOnly(True)
		self.app_title.setStyleSheet("""#AppTitle{
										background: transparent;
										border: none;
										color: #e0e0e0;
										}
										#AppTitle::hover{
											background: #707070;
										}""")

	def save_info(self):
		username = self.username_input.text()
		password = self.password_input.text()
		command = None
		if self.save_btn.text() != 'Saved':
			if self.is_new:
				command = self.is_eligible()
				if command == 'add':
					self.db.register_app(self.app_title.text(), self.icon_url)
					self.db.register_app_account(self.user_id, self.app_id, username, password)
					self.is_new = False
				elif command == 'already exist':
					self.handle_error(command)
				elif command == 'unhidden':
					self.unhidden_app()
					self.is_new = False

			else:
				self.db.update_app_account(self.user_id, self.app_id, password, username)

			if command != 'already exist':
				self.app_icon.save_app_info()
				self.parent.update_app_icon()
				self.mparent.parent.m_pages["Menu"].generate_popup.update_app_items()
				self.save_btn.setText("Saved")
				self.old_user = username
				self.old_pass = password

	def handle_error(self, error=None, username=None, password=None):
		if error == 'already exist':
			self.error.setText("The app is already exist!")
			self.error.show()

	def is_eligible(self):
		apps_id = self.get_apps_id()
		apps_name = self.get_apps_name()
		for user_app, main_app in zip(apps_id, apps_name):
			app_id = main_app[0]
			app_name = main_app[1]
			self.user_app_id = user_app[0]
			is_hidden = user_app[1]
			if self.app_title.text().lower() == app_name:
				if app_id == self.user_app_id:
					if is_hidden:
						return "unhidden"
					else:
						return "already exist"
		return "add"

	def get_apps_id(self):
		with self.db.conn:
			self.db.cursor.execute("SELECT app_id, is_hidden FROM accounts WHERE user_id = ?", (self.user_id,))
		return self.db.cursor.fetchall()

	def get_apps_name(self):
		with self.db.conn:
			self.db.cursor.execute("SELECT id, name FROM apps")
		return self.db.cursor.fetchall()

	def unhidden_app(self):
		with self.db.conn:
			self.db.cursor.execute("UPDATE accounts SET is_hidden = 0 WHERE user_id = ? AND app_id = ?", (self.user_id, self.user_app_id))
		
		app_id = self.db.get_app_id(self.app_title.text().lower())[0]
		self.mparent.password_list.main_layout.removeWidget(self.parent)
		self.mparent.password_list.main_layout.insertWidget(app_id+1, self.parent, alignment=Qt.AlignCenter)

	def value_changed(self, value, obj=None):
		if obj:
			self.adapt_size()
		if self.save_btn.text() == 'Saved':
			self.save_btn.setText("Save")

	def adapt_size(self):
		text = self.app_title.text()
		font = QFont("MS Shell Dlg 2", 19)
		fm = QFontMetrics(font)
		w = fm.width(text)
		h = fm.height()
		self.app_title.setFixedSize(w+3, h)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.close_layout = QHBoxLayout()
		self.title_layout = QHBoxLayout()
		self.main_form = QHBoxLayout()
		self.form_layout = QFormLayout()
		self.field_layout = QHBoxLayout()
		self.field_layout_2 = QHBoxLayout()
		self.button_layout = QHBoxLayout()
		self.spacer = QLabel()
		self.spacer_2 = QLabel()

		self.close_layout.addWidget(self.close_btn, alignment=Qt.AlignBottom | Qt.AlignRight)
		self.close_layout.addSpacing(20)
		self.main_layout.addSpacing(25)
		self.main_layout.addLayout(self.close_layout)
		self.title_layout.addWidget(self.app_icon, alignment=Qt.AlignRight | Qt.AlignBottom)
		self.title_layout.addWidget(self.app_title, alignment=Qt.AlignLeft | Qt.AlignBottom)
		self.title_layout.addSpacing(80)
		self.button_layout.addWidget(self.toggle_password)
		self.button_layout.addWidget(self.reload_btn)
		self.button_layout.addWidget(self.copy_btn_2)
		self.button_layout.setSpacing(0)
		self.button_layout.setContentsMargins(0, 0, 0, 0)
		self.field_layout.addWidget(self.username_input)
		self.field_layout.addWidget(self.copy_btn)
		self.field_layout_2.addWidget(self.password_input)
		self.field_layout_2.addLayout(self.button_layout)
		self.field_layout_2.addSpacing(10)
		self.form_layout.addRow(self.username, self.field_layout)
		self.form_layout.addRow(self.spacer, self.spacer_2)
		self.form_layout.addRow(self.password, self.field_layout_2)
		self.form_layout.setSpacing(8)
		self.spacer.setFixedSize(10, 4)
		self.spacer_2.setFixedSize(10, 4)
		self.main_form.addSpacing(20)
		self.main_form.addLayout(self.form_layout)
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addSpacing(25)
		self.main_layout.addLayout(self.main_form)
		self.main_layout.addWidget(self.save_btn, alignment=Qt.AlignCenter)
		self.central_widget.setLayout(self.main_layout)

	def setup_stylesheet(self):
		super().setup_stylesheet()
		self.app_title.setObjectName("AppTitle")
		self.save_btn.setStyleSheet("""background: #e0e0e0;
										 color: black;
										 border-radius: 8px;
										 border: 1px solid #424242;""")
		self.setStyleSheet("""QMainWindow{
			                     background-color: transparent;
							     border-image: url('Utils/Assets/key_background.png');
							}
							QPushButton{
								color: #e0e0e0;
								border: none;
							}
							QLabel{
								color: #e0e0e0;
							}
							#AppTitle{
								background: transparent;
								border: none;
								color: #e0e0e0;
							}
							#AppTitle::hover{
								background: #707070;
							}
							QLineEdit{
								color: #e0e0e0;
								background: #5a5a5a;
								border: 1px solid gray;
								lineedit-password-character: 9679;
							}""")

	def eventFilter(self, obj, event):
		if event.type() == QEvent.MouseButtonPress:
			if event.button() == Qt.LeftButton:
				if obj == self.app_title:
					self.app_title.setReadOnly(False)
					self.app_title.setStyleSheet("background: #707070;")
				else:
					self.unfocus_input()
		return super().eventFilter(obj, event)
