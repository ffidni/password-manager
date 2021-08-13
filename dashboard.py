from Utils.popup import *


class ClickableApp(QPushButton):

	def __init__(self, parent=None):
		super().__init__()
		self.parent = parent
		self.init_ui()

	def init_ui(self):
		if self.parent.is_new:
			self.parent.icon_url = "Utils/Assets/unknown.png"
		else:
			self.parent.icon_url = self.parent.db.get_icon(self.parent.app_id)[0]
		self.parent.is_exist = False
		self.setIcon(QIcon(self.parent.icon_url))
		self.setIconSize(QSize(24, 24))
		self.setText("View Password")
		self.clicked.connect(self.parent.view_password)
		self.setFont(QFont("Bahnschrift Light", 11))
		self.setup_stylesheet()
		if self.parent.is_new:
			self.parent.view_password()

	def setup_stylesheet(self):
		self.setStyleSheet("""QPushButton{
								color: #e0e0e0;
								background: transparent;
							}""")


class AppWidget(QFrame):

	def __init__(self, user_id, app_id, app_name, password, is_new=False, parent=None):
		super().__init__()
		self.user_id = user_id
		self.app_id = app_id
		self.app_name = app_name
		self.password = password
		self.is_new = is_new
		self.parent = parent
		self.is_exist = None
		self.db = self.parent.db
		self.setFixedHeight(40)
		self.installEventFilter(self)
		self.setCursor(QCursor(Qt.PointingHandCursor))
		self.init_ui()

	def init_ui(self):
		self.widget_management()
		self.layout_management()

	def widget_management(self):
		self.app_button = ClickableApp(self)
		self.delete_button = DeleteButton(icon="Utils/Assets/delete.png", cursor=QCursor(Qt.PointingHandCursor), widget=self, parent=self.parent, is_app=True)
		self.delete_button.hide()

	def layout_management(self):
		self.main_layout = QHBoxLayout()

		self.main_layout.addWidget(self.app_button, alignment=Qt.AlignRight)
		self.main_layout.addWidget(self.delete_button, alignment=Qt.AlignLeft)
		self.setLayout(self.main_layout)

	def view_password(self):
		if self.is_exist:
			self.password_info.show()
		else:
			app_info = self.parent.db.get_app_account(self.user_id, self.app_id)
			if self.is_new:
				self.password_info = AppPass(self.user_id, self.app_id, self.app_name, self.parent, self, self.icon_url, self.is_new)
			else:
				self.password_info = AppPass(self.user_id, self.app_id, self.app_name, self.parent, self)
			if app_info and (app_info[0] or app_info[1]) and not app_info[2]:
				self.password_info.username_input.setText(app_info[0])
				self.password_info.password_input.setText(app_info[1])
				self.password_info.old_user = app_info[0]
				self.password_info.old_pass = app_info[1]

			self.password_info.password_input.setEchoMode(QLineEdit.Password)
			center_popup(self.password_info, self.parent.width(), self.parent.height())
			self.password_info.show()
			self.is_exist = True

	def update_app_icon(self):
		self.is_new = False
		self.icon_url = self.password_info.app_icon.current_img
		self.app_button.setIcon(QIcon(self.icon_url))

	def eventFilter(self, obj, event):
		if event.type() == QEvent.Enter:
			self.delete_button.show()
			self.setStyleSheet("background: #3a5969;")
		elif event.type() == QEvent.Leave:
			self.delete_button.hide()
			self.setStyleSheet("background: transparent;")
		elif event.type() == QEvent.MouseButtonPress:
			if event.button() == Qt.LeftButton:
				self.view_password()

		return super().eventFilter(obj, event)


class PasswordList(QScrollArea):

	def __init__(self, user_id, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.user_id = user_id
		self.app_id = None
		self.db = self.parent.db
		self.current_opened = None
		self.setFixedSize(206, 242)
		self.init_ui()
		
	def init_ui(self):
		self.setup_widget()
		self.setup_stylesheet()
		self.setup_layout()

	def setup_widget(self):
		self.main = QWidget()

		self.title = QLabel("Password List")
		self.apps = self.db.get_app()
		self.accounts = self.db.get_accounts(self.user_id)

		for idx, app in enumerate(self.apps):
			app_id = app[0]
			app_name = app[1]
			var_app_name = app_name.replace(" ", "_")
			try:
				password = self.accounts[idx][4]
				is_hidden = self.accounts[idx][5]
				if not is_hidden:
					exec(f"self.{var_app_name} = AppWidget(self.user_id, {app_id}, app_name, {bool(password)}, parent=self.parent)")
			except:
				pass

		self.add_button = AddButton(icon=QIcon("Utils/Assets/new.png"), cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.add_button.clicked.connect(lambda: self.add_new("New App", "Utils/Assets/unknown.png", ""))
		self.title.setFont(QFont("MS Shell Dlg 2", 14))
		self.add_button.setIconSize(QSize(24, 24))
		self.add_button.setFixedSize(24, 24)

	def setup_stylesheet(self):
		self.setObjectName("Main")
		self.setStyleSheet( """
		#Main{
			background: #3e6578;
			border: 1px solid #424242;
			border-radius: 8px;
		}
		QWidget{
			background: #3e6578;
			border-radius: 8px;
		}
    	QScrollArea {
    		background: transparent;
    	    border: none;
    	}

    	QScrollBar {
    	    background: #bdbdbd;
    	    border-radius: 5px;
    	}

    	QScrollBar:horizontal {
    	    height: 13px;
    	}

    	QScrollBar:vertical {
    		background: #9e9e9e;
    	    width: 13px;
    	}

    	QScrollBar::add-page:vertical{
    		background: #757575;
    	}

    	QScrollBar::sub-page:vertical{
    		background: #757575;
    	}

    	QScrollBar::add-page:horizontal{
    		background: #bdbdbd;
    	}

    	QScrollBar::sub-page:horizontal{
    		background: #bdbdbd;
    	}

    	QScrollBar::handle {
    	    border-radius: 5px;
    	}

    	QScrollBar::handle:horizontal {
    	    height: 25px;
    	    min-width: 10px;
    	}

    	QScrollBar::handle:vertical {
    	    width: 25px;
    	    min-height: 10px;
    	}

    	QScrollBar::add-line {
    	    border: none;
    	    background: none;
    	}

    	QScrollBar::sub-line {
    	    border: none;
    	    background: none;
    	}
    	""")
		self.title.setStyleSheet("color: #e0e0e0;")

	def setup_layout(self):
		self.main_layout = QVBoxLayout()

		self.main_layout.addSpacing(10)
		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		for idx, app in enumerate(self.apps):
			app_id = app[0]
			app_name = app[1]
			var_app_name = app_name.replace(" ", "_")
			try:
				password = self.accounts[idx][4]
				is_hidden = self.accounts[idx][5]
				if not is_hidden:
					self.main_layout.addWidget(eval(f"self.{var_app_name}"), alignment=Qt.AlignCenter)
			except:
				pass
	
		self.main_layout.addWidget(self.add_button, alignment=Qt.AlignRight)
		self.main_layout.setSpacing(0)
		self.main.setLayout(self.main_layout)
		self.setWidget(self.main)
		self.setWidgetResizable(True)

	def add_new(self, app_title, app_icon, password=""):
		self.layout_idx = self.db.get_app(self.user_id, True)[0]+2
		self.app_id = self.db.count_id()[0]+1
		var_app_name = app_title.replace(" ", "_")
		exec(f"self.{var_app_name} = AppWidget(self.user_id, {self.app_id}, app_title, {bool(password)}, True, parent=self.parent)")
		self.main_layout.insertWidget(self.layout_idx, eval(f"self.{var_app_name}"), alignment=Qt.AlignCenter)


class HotkeyList(QScrollArea):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.hotkeys = self.parent.parent.hotkeys
		self.setFixedSize(206, 242)
		self.init_ui()

	def init_ui(self):
		self.setup_widget()
		self.setup_stylesheet()
		self.setup_layout()

	def setup_widget(self):
		self.title = QLabel("Hotkey Settings")
		self.open_pass = QLabel("Open Password\nGenerator:")
		self.open_pass_key = QLineEdit(self.hotkeys[0][0])
		self.open_list = QLabel("Go to\nDashboard:")
		self.open_list_key = QLineEdit(self.hotkeys[0][1])
		self.switch_account = QLabel("Switch Account:")
		self.switch_account_key = QLineEdit(self.hotkeys[0][2])
		self.hotkey_popup = HotkeyPopup(self.parent.parent)

		self.title.setFont(QFont("MS Shell Dlg 2", 14))
		self.open_pass_key.setReadOnly(True)
		self.open_list_key.setReadOnly(True)
		self.switch_account_key.setReadOnly(True)
		self.open_pass_key.setObjectName("gen")
		self.open_list_key.setObjectName("list")
		self.switch_account_key.setObjectName("switch")

	def setup_stylesheet(self):
		for name in ('open_pass', 'open_list', 'switch_account'):
			eval(f"self.{name}.setFont(QFont('Bahnschrift Light', 11))")
			eval(f"self.{name}.setStyleSheet('color: #e0e0e0;')")
			eval(f"self.{name}_key.setFont(QFont('Bahnschrift Light', 10))")
			eval(f"self.{name}_key.setFixedWidth(80)")
			eval(f"self.{name}_key.setAlignment(Qt.AlignCenter)")
			eval(f"self.{name}_key.setCursor(QCursor(Qt.PointingHandCursor))")
			eval(f"self.{name}_key.installEventFilter(self)")

		self.setObjectName("Main")
		self.setStyleSheet("""#Main{background: #3e6578;
							  border: 1px solid #424242;
							  border-radius: 8px;}
							  QLineEdit{
							 	color: #bdbdbd;
							  	background: #426b7f;
							  	border: 1.1px solid #424242;
							  	border-radius: 4px;
							  }
							  QLineEdit::hover{
							  	background: #467389;
							  }""")
		self.title.setStyleSheet("color: #e0e0e0;")

	def setup_layout(self):
		self.main_layout = QVBoxLayout()
		self.form_layout = QFormLayout()

		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		self.main_layout.addSpacing(12)
		for name in ('open_pass', 'open_list', 'switch_account'):
			self.form_layout.addRow(eval(f"self.{name}"), eval(f"self.{name}_key"))
			spacer1, spacer2 = QLabel(), QLabel()
			spacer1.setFixedHeight(6)
			spacer2.setFixedHeight(6)
			self.form_layout.addRow(spacer1, spacer2)

		self.main_layout.addLayout(self.form_layout)
		self.main_layout.addSpacing(15)
		self.setLayout(self.main_layout)

	def eventFilter(self, obj, event):
		if event.type() == QEvent.MouseButtonPress:
			if obj in (self.open_pass_key, self.open_list_key, 
						self.switch_account_key):
				self.hotkey_popup.show(obj.objectName(), obj)

		return super().eventFilter(obj, event)


class AccountWidget(QFrame):

	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.user_icon = UserButton(icon=QIcon("Utils/Assets/user.png"), cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.account_info = QLabel(f"Username: {self.parent.username}\nEmail: {self.parent.email}")
		self.edit_btn = EditButton(icon="Utils/Assets/pencil.png", cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.edit_btn.clicked.connect(self.edit_account)
		self.installEventFilter(self)
		self.init_ui()

	def edit_account(self):
		dashboard = self.parent
		dashboard.account_edit.show()
		dashboard.account_edit.user_id = dashboard.current_user_id
		dashboard.account_edit.username_input.setText(dashboard.username)
		dashboard.account_edit.email_input.setText(dashboard.email)
		dashboard.account_edit.list_item = None
		dashboard.account_edit.account_info = f"{self.parent.username}\n{self.parent.email}"

	def init_ui(self):
		self.main_layout = QHBoxLayout()

		self.main_layout.addSpacing(10)
		self.main_layout.addWidget(self.user_icon, alignment=Qt.AlignRight)
		self.main_layout.addSpacing(8)
		self.main_layout.addWidget(self.account_info, alignment=Qt.AlignCenter)
		self.main_layout.addWidget(self.edit_btn, alignment=Qt.AlignLeft)
		self.setLayout(self.main_layout)
		self.setup_stylesheet()

	def setup_stylesheet(self):
		self.setObjectName("Main")
		self.setStyleSheet("""#Main{
							   background: transparent;
							   border: none;
							   border-radius: 15px;
							   }
							  QLabel{
							   color: #e0e0e0;
						      }""")

	def eventFilter(self, obj, event):
		if event.type() == QEvent.Enter:
			self.user_icon.setIcon(QIcon("Utils/Assets/user_text.png"))
			self.setStyleSheet("""#Main{
								   background: #3e6578;
								   border: none;
								   border-radius: 15px;
								   }
								  QLabel{
								   color: #e0e0e0;
							      }""")
		elif event.type() == QEvent.Leave:
			self.user_icon.setIcon(QIcon("Utils/Assets/user.png"))
			self.setStyleSheet("""#Main{
								   background: transparent;
								   border: none;
								   border-radius: 15px;
								   }
								  QLabel{
								   color: #e0e0e0;
							      }""")

		return super().eventFilter(obj, event)


class Dashboard(QWidget):
	goto_signal = pyqtSignal(str)

	def __init__(self, user_id=1, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.db = Database("Utils/data.db")
		self.current_user_id = user_id
		self.init_ui()

	def init_ui(self):
		self.setup_widget()
		self.setup_stylesheet()
		self.setup_layout()

	def new_passwords(self, user_id):
		account_info = self.db.get_users(user_id)
		self.username = account_info[1]
		self.email = account_info[2]
		self.board_layout.removeWidget(self.password_list)
		self.password_list.deleteLater()
		self.password_list = PasswordList(user_id, self)
		self.password_list.installEventFilter(self)
		self.board_layout.insertWidget(0, self.password_list, alignment=Qt.AlignRight)

	def setup_widget(self):
		account_info = self.db.get_users(self.current_user_id)
		try:
			self.username = account_info[1]
			self.email = account_info[2]
		except:
			self.username = ""
			self.email = ""
		
		self.account_widget = AccountWidget(self)
		self.back_btn = BackButton(icon=QIcon("Utils/Assets/back.png"), cursor=QCursor(Qt.PointingHandCursor), parent=self)
		self.line = QFrame(self)
		self.hotkeys = HotkeyList(self)
		self.password_list = PasswordList(self.current_user_id, self)

		self.password_list.installEventFilter(self)
		self.hotkeys.installEventFilter(self)
		self.back_btn.setIconSize(QSize(32, 32))
		self.back_btn.setFixedSize(32, 32)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFixedWidth(410)
		self.account_widget.account_info.setFont(QFont("MS Shell Dlg 2", 12))
		self.account_widget.user_icon.clicked.connect(self.show_accounts)

	def eventFilter(self, obj, event):
		if event.type() == QEvent.Enter:
			if obj in (self.password_list, self.hotkeys):
				shadow = QGraphicsDropShadowEffect()
				shadow.setBlurRadius(15)
				obj.setGraphicsEffect(shadow)
		elif event.type() == QEvent.Leave:
			if obj in (self.password_list, self.hotkeys):
				obj.setGraphicsEffect(None)

		return super().eventFilter(obj, event)

	def show_accounts(self):
		self.account_list.show()

	def setup_stylesheet(self):
		self.line.setStyleSheet("color: #424242;")

	def setup_layout(self):
		self.main_layout = QVBoxLayout()
		self.account_layout = QHBoxLayout()
		widget = QWidget()
		self.board_layout = QHBoxLayout()
		self.board_widget = QWidget()

		self.main_layout.addSpacing(70)
		self.account_layout.addWidget(self.back_btn, alignment=Qt.AlignRight)
		self.account_layout.addWidget(self.account_widget, alignment=Qt.AlignLeft)
		widget.setLayout(self.account_layout)
		self.main_layout.addWidget(widget, alignment=Qt.AlignCenter)
		self.main_layout.addWidget(self.line, alignment=Qt.AlignCenter)
		self.board_layout.addWidget(self.password_list, alignment=Qt.AlignRight)
		self.board_layout.addSpacing(15)
		self.board_layout.addWidget(self.hotkeys, alignment=Qt.AlignLeft)
		self.board_widget.setLayout(self.board_layout)
		self.main_layout.addWidget(self.board_widget, alignment=Qt.AlignCenter | Qt.AlignTop)
		self.main_layout.addSpacing(60)
		self.setLayout(self.main_layout)
		self.account_list = SwitchAccount(self)
		self.account_edit = CreateAccount(parent=self, is_edit=True)
		self.account_edit.hide()
		self.account_list.hide()
		width, height = self.parent.width(), self.parent.height()
		center_popup(self.account_list, width, height)
		center_popup(self.account_edit, width, height)
