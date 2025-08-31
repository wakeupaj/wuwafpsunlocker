import os
import sqlite3
import sys
from PySide6.QtCore import (QMetaObject, QRect)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QFileDialog, QDialog, QLabel, QVBoxLayout,
                               QDialogButtonBox)


class ErrorDialog(QDialog):
    def __init__(self, parent=None, text='', types='Error'):
        super(ErrorDialog, self).__init__(parent)
        self.setWindowIcon(QIcon("wuwafulogo.ico"))
        label = QLabel(text)
        layout = QVBoxLayout()
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.close)
        self.setWindowTitle(types)
        layout.addWidget(label)
        layout.addWidget(buttons)
        self.setLayout(layout)


class Ui_fpsunlocker(object):
    def setupUi(self, fpsunlocker):
        if not fpsunlocker.objectName():
            fpsunlocker.setObjectName("fpsunlocker")
            fpsunlocker.setWindowIcon(QIcon("wuwafulogo.ico"))
        fpsunlocker.resize(307, 273)
        fpsunlocker.setStyleSheet("QWidget{background: #3d3d3d; color: White;}")
        self.select_folder_btn = QPushButton(fpsunlocker)
        self.select_folder_btn.setObjectName("select_folder_btn")
        self.select_folder_btn.setGeometry(QRect(90, 40, 131, 51))
        self.select_folder_btn.setStyleSheet("QPushButton{background: #1a1a1a; color: White;}")
        self.select_folder_btn.clicked.connect(self._init_btn)
        self.unlock_btn = QPushButton(fpsunlocker)
        self.unlock_btn.setObjectName("unlock_btn")
        self.unlock_btn.setGeometry(QRect(90, 160, 131, 51))
        self.unlock_btn.setStyleSheet("QPushButton{background: #1a1a1a; color: White;}")
        self.unlock_btn.clicked.connect(self._btnState)
        self._db_path = ''

        self.retranslateUi(fpsunlocker)

        QMetaObject.connectSlotsByName(fpsunlocker)
    # setupUi

    def retranslateUi(self, fpsunlocker):
        fpsunlocker.setWindowTitle("WuWa FPS Unlocker")
        self.select_folder_btn.setText("Select Folder")
        self.unlock_btn.setText("Unlock 120FPS")
        self.unlock_btn.setDisabled(True)
        if os.path.exists(os.path.join(os.getcwd(), 'check_state.txt')):
            if open(os.path.join(os.getcwd(), 'check_state.txt'), 'r', encoding='utf-8').read() == 'unchecked':
                self.unlock_btn.setText('Disabled')
            else:
                self.unlock_btn.setText('Unlock 120FPS')

    def update_fps_to_max(self):
        if self._db_path != '':
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE LocalStorage SET Value = 120 WHERE Key = 'CustomFrameRate'")
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    def undo_fps(self):
        if self._db_path != '':
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE LocalStorage SET Value = 60 WHERE Key = 'CustomFrameRate'")
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    def select_folder(self):
        if os.path.exists(os.path.join(os.getcwd(), 'path_config.txt')):
            dirs = open(os.path.join(os.getcwd(), 'path_config.txt'), 'r', encoding='utf-8').read()
        else:
            dirs = os.path.expanduser('~')
        path = QFileDialog.getExistingDirectory(None, caption='Open Directory', dir=dirs)
        if path != '':
            if path is not None:
                with open(os.path.join(os.getcwd(), 'path_config.txt'), 'w', encoding='utf-8') as w:
                    w.write(path)
                db_path = os.path.join(path, 'Client', 'Saved', 'LocalStorage', 'LocalStorage.db')
                if os.path.exists(db_path):
                    if os.path.isfile(db_path):
                        return db_path
                    else:
                        ErrorDialog(types="Error", text='The LocalStorage.db file was not found in the selected directory.').exec()
                        return ''
                else:
                    return ''
            else:
                return ''
        else:
            return ''

    def _init_btn(self, _):
        self._db_path = self.select_folder()
        if self._db_path != '':
            self.unlock_btn.setEnabled(True)
        else:
            self.unlock_btn.setDisabled(True)

    def _btnState(self, _):
        if os.path.exists(os.path.join(os.getcwd(), 'check_state.txt')):
            if open(os.path.join(os.getcwd(), 'check_state.txt'), 'r', encoding='utf-8').read() == 'checked':
                self.unlock_btn.setText('Disabled')
                with open(os.path.join(os.getcwd(), 'check_state.txt'), 'w', encoding='utf-8') as w:
                    w.write('unchecked')
                self.update_fps_to_max()
                ErrorDialog(types="Success", text='FPS set to maximum successfully!').exec()
            else:
                self.unlock_btn.setText('Unlock 120FPS')
                with open(os.path.join(os.getcwd(), 'check_state.txt'), 'w', encoding='utf-8') as w:
                    w.write('checked')
                self.undo_fps()
                ErrorDialog(types="Success", text='FPS recovery successfully!').exec()
        else:
            with open(os.path.join(os.getcwd(), 'check_state.txt'), 'w', encoding='utf-8') as w:
                w.write('unchecked')
            self.unlock_btn.setText('Disabled')
            self.update_fps_to_max()
            ErrorDialog(types="Success", text='FPS set to maximum successfully!').exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_fpsunlocker()
    ui.setupUi(main_window)
    main_window.setFixedSize(main_window.size())
    main_window.show()
    sys.exit(app.exec())