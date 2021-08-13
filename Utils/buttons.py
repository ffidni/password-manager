from Utils.packages import *
from Utils.functions import goto_dashboard

class Button(QPushButton):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(parent)
		self.setStyleSheet("background: transparent;")
		self.setIcon(QIcon(icon))
		self.setCursor(cursor)
		self.setFocusPolicy(Qt.NoFocus)

class EditButton(Button):

	def __init__(self, icon, cursor, widget=None, parent=None):
		super().__init__(icon, cursor, parent)
		self.widget = widget
		self.setIconSize(QSize(32, 32))
		self.setToolTip("Edit account's info")


class DeleteButton(Button):

	def __init__(self, icon, cursor, widget=None, parent=None, user_id=None, is_app=False):
		super().__init__(icon, cursor, parent)
		self.parent = parent #.parent for dashboard widget
		self.app_widget = widget
		self.list_widget = None
		self.db = self.parent.db
		self.is_app = is_app
		self.user_id = user_id
		self.setFixedSize(14, 14)
		self.setIconSize(QSize(14, 14))
		self.clicked.connect(self.remove)

	def remove(self):
		if self.is_app:
			password_list = self.parent.password_list
			user_id = self.app_widget.user_id
			app_id = self.app_widget.app_id
			password_list.main_layout.removeWidget(self.app_widget)
			self.db.update_app_account(user_id, app_id, "", "")
			self.parent.parent.m_pages["Menu"].generate_popup.save_input.removeItem(app_id-1)
			self.app_widget.deleteLater()
			self.db.remove_app(user_id, app_id)
		else:
			self.main_list = self.parent.list
			self.db.remove_account(self.user_id)
			if self.list_widget.widget.user_id == self.parent.parent.current_user_id:
				curr_row = self.main_list.currentRow()
				prev_item = self.main_list.item(curr_row-1)
				next_item = self.main_list.item(curr_row+1)
				if prev_item and not next_item:
					self.parent.switch_account(prev_item)
					self.main_list.takeItem(self.main_list.row(self.list_widget))
				elif not prev_item and next_item:
					self.parent.switch_account(next_item)
					self.main_list.takeItem(self.main_list.row(self.list_widget))
				else:
					self.hide()
					self.main_list.takeItem(curr_row)
					main = self.parent.parent.parent
					main.user_exist = False
					main.setCurrentWidget(main.m_pages["Menu"])
					main.generate_pass()
			else:
				self.main_list.takeItem(self.main_list.row(self.list_widget))


class AppButton(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)
		self.app_id = parent.app_id
		self.parent = parent
		self.db = parent.db
		self.clicked.connect(self.change_icon)
		self.old_img = icon
		self.current_img = self.old_img

		self.setFixedSize(32, 32)
		self.setIconSize(QSize(32, 32))
		self.setStyleSheet(f"""QPushButton::hover{{
							      background: solid #707070;
							      border-radius: {self.width()//2}px;
			}}""")

	def change_icon(self):
		file_name = QFileDialog.getOpenFileName(self, "Open file", "C:/", "Image files (*)")
		self.current_img = file_name[0]
		if self.current_img:
			if self.current_img != self.old_img:
				self.parent.save_btn.setText("Save")
		else:
			self.current_img = old_img
		self.setIcon(QIcon(self.current_img))

	def save_app_info(self):
		with self.db.conn:
			self.db.cursor.execute("UPDATE apps SET icon_url = ? WHERE id = ?", (self.current_img, self.app_id))
			self.db.cursor.execute("UPDATE apps SET name = ? WHERE id = ?", (self.parent.app_title.text().lower(), self.app_id))


class TogglePassword(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)
		self.parent = parent
		self.hidden = True
		self.clicked.connect(self.click_event)
		self.setFixedSize(18, 18)
		self.setIconSize(QSize(18, 18))
		self.setStyleSheet(f"""QPushButton::hover{{
							      background: solid #707070;
							      border-radius: {self.width()//2}px;
			}}""")

	def click_event(self, event):
		if self.hidden:
			self.hidden = False
			self.parent.password_input.setEchoMode(QLineEdit.Normal)
			self.setIcon(QIcon("Utils/Assets/show_password.png"))
		else:
			self.hidden = True
			self.parent.password_input.setEchoMode(QLineEdit.Password)
			self.setIcon(QIcon("Utils/Assets/hide_password.png"))


class BackButton(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)
		self.parent = parent
		self.clicked.connect(self.back)

	def back(self):
		self.parent.goto_signal.emit("Menu")


class UserButton(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)
		self.parent = parent
		self.setToolTip("Switch account")
		self.setIconSize(QSize(36, 36))
		self.setFixedSize(36, 36)
		self.setStyleSheet(""" QPushButton{
							    	background: transparent;
								}""")


class CloseButton(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)
		self.clicked.connect(parent.hide)


class CopyButton(Button):

	def __init__(self, icon, cursor, input_field, parent=None):
		super().__init__(icon, cursor, parent)
		self.parent = parent
		self.clicked.connect(lambda: self.copy_clipboard(input_field))
		self.setFixedSize(22, 22)
		self.setIconSize(QSize(22, 22))
		self.setStyleSheet(f"""QPushButton::hover{{
							      background: solid #707070;
							      border-radius: {self.width()//2}px;
			}}""")

	def change_icon(self, icon_url):
		self.setIcon(QIcon(icon_url))

	def copy_clipboard(self, input_field):
		hidden = False
		if input_field == 2:
			input_field.setEchoMode(QLineEdit.Normal)
			hidden = True

		input_field.selectAll()
		input_field.copy()
		input_field.deselect()
		self.change_icon("Utils/Assets/copied.png")
		QTimer.singleShot(800, lambda: self.change_icon("Utils/Assets/copy.png"))
		if hidden:
			input_field.setEchoMode(QLineEdit.Password)


class AddButton(Button):

	def __init__(self, icon, cursor, parent=None):
		super().__init__(icon, cursor, parent)


class ReloadButton(Button):

	def __init__(self, icon, cursor, input_field, length_field=12, is_adapt=True, parent=None):
		super().__init__(icon, cursor, parent)
		self.parent = parent
		self.is_adapt = is_adapt
		self.input_field = input_field
		self.length_field = length_field
		self.allowed_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~`!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/0123456789'
		self.clicked.connect(lambda: self.generate_pass(self.length_field.value()))
		self.setFixedSize(18, 18)
		self.setIconSize(QSize(18, 18))
		self.setToolTip("Generate new password")
		self.setStyleSheet(f"""QPushButton::hover{{
							      background: solid #707070;
							      border-radius: {self.width()//2}px;
			}}""")

	def generate_pass(self, length):
		if self.length_field.isHidden():
			length_layout = QHBoxLayout()
			length_layout.addWidget(self.parent.length_text, alignment=Qt.AlignRight)
			length_layout.addWidget(self.parent.length_input, alignment=Qt.AlignLeft)
			self.parent.main_layout.itemAt(0).changeSize(0, 45)
			self.parent.main_layout.insertLayout(5, length_layout)
			self.length_field.show()
			self.parent.length_text.show()

		result = ''.join(choice(self.allowed_char) for _ in range(length))
		self.input_field.setText(result)
		self.adapt_size(result)

	def hide_length(self):
		self.parent.length_text.hide()
		self.length_field.hide()
		self.parent.main_layout.itemAt(0).changeSize(0, 25)

	def adapt_size(self, text):
		if self.is_adapt:
			length = len(text)
			if length <= 30:
				font = QFont("Bahnschrift Light", 0)
				fm = QFontMetrics(font)
				w = fm.width(text)
				h = fm.height()
				if length > 13:
					self.input_field.setFixedSize(w+30, self.input_field.height())
			else:
				self.input_field.setFixedSize(228, self.input_field.height())
