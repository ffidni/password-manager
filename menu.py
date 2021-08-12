from Utils.popup import *
from dashboard import *

class Menu(QWidget):
	goto_signal = pyqtSignal(str)

	def __init__(self, user_id, parent):
		super().__init__(parent)
		self.parent = parent
		self.current_user_id = user_id
		self.init_ui()

	def init_ui(self):
		self.setup_widget()
		self.setup_style()
		self.setup_layout()
		self.db = Database("Utils/data.db")
		self.user_exist = self.parent.user_exist
		if self.user_exist:
			self.create_acc = CreateAccount(self)
		else:
			self.create_acc = CreateAccount(parent=self, first=True)

		self.generate_popup = GenerateResult(self)
		self.generate_popup.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
		self.generate_popup.hide()

	def show_register(self):
		center_popup(self.create_acc, self.parent.width(), self.parent.height())
		self.create_acc.show()

	def on_click(self, event):
		if self.user_exist:
			if event == 'generate':
				self.parent.generate_pass()
			elif event == 'dashboard':
				self.goto_signal.emit("Dashboard")
		else:
			self.show_register()
		
	def setup_widget(self):
		self.title = QLabel("Password Manager")
		self.lock_icon = QPushButton(icon=QIcon("Utils/Assets/lock.png"), cursor=QCursor(Qt.PointingHandCursor))
		self.ver_line = QFrame()
		self.key_icon = QPushButton(icon=QIcon("Utils/Assets/key.png"), cursor=QCursor(Qt.PointingHandCursor))
		self.generate_text = QLabel("Generate Secure Password")
		self.dashboard_text = QLabel("Dashboard")
		
		self.title.setFont(QFont("MS Shell Dlg 2", 37))
		self.generate_text.setWordWrap(True)
		self.generate_text.setAlignment(Qt.AlignCenter)
		self.generate_text.setFont(QFont("MS Shell Dlg 2", 14))
		self.dashboard_text.setFont(QFont("MS Shell Dlg 2", 14))
		self.lock_icon.clicked.connect(lambda: self.on_click('generate'))
		self.lock_icon.setIconSize(QSize(140, 152))
		self.key_icon.clicked.connect(lambda: self.on_click("dashboard"))
		self.key_icon.setIconSize(QSize(98, 152))
		self.ver_line.setFrameShape(QFrame.VLine)
		
	def setup_layout(self):
		self.main_layout = QVBoxLayout()
		self.icon_layout = QHBoxLayout()
		self.generate_layout = QVBoxLayout()
		self.dashboard_layout = QVBoxLayout()

		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		self.generate_layout.addWidget(self.lock_icon, alignment=Qt.AlignBottom | Qt.AlignCenter)
		self.generate_layout.addWidget(self.generate_text, alignment=Qt.AlignTop | Qt.AlignCenter)
		self.dashboard_layout.addWidget(self.key_icon, alignment=Qt.AlignBottom | Qt.AlignCenter)
		self.dashboard_layout.addWidget(self.dashboard_text, alignment=Qt.AlignTop | Qt.AlignCenter)
		self.icon_layout.addSpacing(100)
		self.icon_layout.addLayout(self.generate_layout)
		self.icon_layout.addWidget(self.ver_line)
		self.icon_layout.addLayout(self.dashboard_layout)
		self.icon_layout.addSpacing(100)
		self.main_layout.addLayout(self.icon_layout)
		self.main_layout.addSpacing(75)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.main_layout)

	def setup_style(self):
		self.title.setStyleSheet("""color: #f5f5f5;""")
		self.lock_icon.setStyleSheet("""background: transparent;""")
		self.ver_line.setStyleSheet("color: #424242;")
		self.key_icon.setStyleSheet("""background: transparent;""")
		self.generate_text.setStyleSheet("color: #e0e0e0;")
		self.dashboard_text.setStyleSheet("color: #e0e0e0;")

class HotkeyThread(QThread):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.generate_pass = self.parent.generate_pass
		self.show_list = self.parent.show_list
		self.switch_popup = self.parent.switch_popup
		self.hotkeys = self.parent.hotkeys

	def run(self):
		with GlobalHotKeys({
			self.hotkeys[1][0]: self.generate_pass,
			self.hotkeys[1][1]: self.show_list,
			self.hotkeys[1][2]: self.switch_popup
			}) as self.l:
				self.l.join()

	def stop(self):
		self.terminate()
		self.l.stop()

class PageSelector(QStackedWidget):

	def __init__(self):
		super().__init__()
		self.w, self.h = 573, 550
		self.w_factor, self.h_factor = 1, 1
		self.db = Database("Utils/data.db")
		self.keyboard = Controller()

		self.user_exist = self.db.get_data("users")
		self.current_popup = None
		self.setWindowTitle("Password Manager")
		self.setWindowIcon(QIcon("Utils/Assets/logo.png"))
		self.setObjectName("Main")
		self.setStyleSheet("""#Main{background: #406b7f;}""")
		self.setFixedSize(self.w, self.h)
		self.installEventFilter(self)
		
		self.hotkeys = self.get_hotkeys()
		self.hotkey_thread = HotkeyThread(self)
		self.hotkey_thread.start()
		self.last_login = self.db.get_last_login()[0]
		self.m_pages = {}

		self.register(Menu(user_id=self.last_login, parent=self), "Menu")
		self.register(Dashboard(user_id=self.last_login, parent=self), "Dashboard")
		self.goto("Menu")

	def get_hotkeys(self):
		result = [[], []]
		for i in range(1, 4):
			hotkey_key = self.db.get_hotkey(i)
			if hotkey_key:
				hotkey_key = hotkey_key[0]
				hotkey_text = hotkey_key.replace("<", "").replace(">", "").title()
				result[0].append(hotkey_text)
				result[1].append(hotkey_key)
			else:
				self.db.register_hotkeys()
				return self.get_hotkeys()
		return result

	def is_active(self, slot=False):
		if not self.isActiveWindow() and not slot:
			self.hide()
			self.showNormal()
			self.activateWindow()
			self.setFocus(True)
			for _ in range(15):
				self.keyboard.press(HotKey.parse("<ctrl>")[0])

	def generate_pass(self):
		if self.user_exist:
			self.is_active()
			if self.currentWidget() != "Menu":
				self.goto("Menu")
			popup = self.m_pages["Menu"].generate_popup
			center_popup(popup, self.width(), self.height())
			popup.show()
			popup.reload_btn.generate_pass(popup.length_input.value())
			new_pass = popup.password.text()
		else:
			self.m_pages["Menu"].show_register()

	def switch_popup(self):
		if self.user_exist:
			self.is_active()
			if self.currentWidget() != "Dashboard":
				self.hide_popup(self.m_pages["Menu"].generate_popup)
				self.goto("Dashboard")
			self.m_pages["Dashboard"].account_widget.user_icon.clicked.emit()
		else:
			self.m_pages["Menu"].show_register()

	def show_list(self):
		if self.user_exist:
			self.is_active()
			if self.currentWidget() != "Dashboard":
				self.hide_popup(self.m_pages["Menu"].generate_popup)
				self.hide_popup(self.m_pages["Dashboard"].account_list)
				self.goto("Dashboard")
		else:
			self.m_pages["Menu"].show_register()

	def hide_popup(self, popup):
		if not popup.isHidden():
			popup.hide()

	def toggle_fullscreen(self):
		if self.isFullScreen():
			self.showNormal()
		else:
			self.max_screen()
			self.showFullScreen()

	def register(self, widget, name):
		self.m_pages[name] = widget
		self.addWidget(widget)
		widget.goto_signal.connect(self.goto)

	@pyqtSlot(str)
	def goto(self, name):
		if name in self.m_pages:
			widget = self.m_pages[name]
			self.setCurrentWidget(widget)

if __name__ == '__main__':
	app = QApplication(argv)
	win = PageSelector()
	win.show()
	exit(app.exec_())