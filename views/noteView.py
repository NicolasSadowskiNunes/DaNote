from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTabWidget, QInputDialog, QMessageBox, QDockWidget,
    QListWidget, QVBoxLayout, QWidget, QToolBar, QFileDialog, QLabel, QListWidgetItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from classes.noteEditor import NoteEditor
import os

class NoteView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DaNote - Your Note App")
        self.setGeometry(100, 100, 800, 600)

        self.create_side_menu()

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.create_vertical_toolbar()

        self.add_initial_note()

    def add_initial_note(self):
        note_name = "Note"
        initial_content = ""
        self.create_note_editor(note_name, initial_content)

    def create_vertical_toolbar(self):
        icons_size = QSize(25, 25)

        self.vertical_toolbar = QToolBar(self)
        self.vertical_toolbar.setMovable(False)
        self.addToolBar(Qt.LeftToolBarArea, self.vertical_toolbar)

        self.add_note_button = QPushButton()
        self.add_note_button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_add.png"))
        self.add_note_button.setFixedSize(30, 30)
        self.add_note_button.setIconSize(icons_size)
        self.add_note_button.clicked.connect(self.add_new_note)
        self.vertical_toolbar.addWidget(self.add_note_button)

        self.open_note_button = QPushButton()
        self.open_note_button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_open.png"))
        self.open_note_button.setFixedSize(30, 30)
        self.open_note_button.clicked.connect(self.open_existing_note)
        self.open_note_button.setIconSize(icons_size)
        self.vertical_toolbar.addWidget(self.open_note_button)

        self.open_folder_button = QPushButton()
        self.open_folder_button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_folderBtn.png"))
        self.open_folder_button.clicked.connect(self.open_folder)
        self.open_folder_button.setFixedSize(30, 30)
        self.open_folder_button.setIconSize(icons_size)
        self.vertical_toolbar.addWidget(self.open_folder_button)

        self.save_note_button = QPushButton()
        self.save_note_button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_save.png"))
        self.save_note_button.setFixedSize(30, 30)
        self.save_note_button.clicked.connect(self.save_current_note)
        self.save_note_button.setIconSize(icons_size)
        self.vertical_toolbar.addWidget(self.save_note_button)

    def create_side_menu(self):
        self.dock = QDockWidget(self)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(500)
        self.file_list.setStyleSheet("""
            background-color: #ecf0f1;
            border: none;
            font-size: 14px;
            color: #34495e;
        """)
        self.file_list.hide()

        self.toggle_menu_button = QPushButton(self)
        self.toggle_menu_button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_menu.png"))
        self.toggle_menu_button.setFixedSize(30, 30)
        self.toggle_menu_button.setIconSize(QSize(30, 30))
        self.toggle_menu_button.clicked.connect(self.toggle_menu)

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)

        menu_layout.addWidget(self.toggle_menu_button)
        menu_layout.addWidget(self.file_list)
        menu_layout.addStretch(1)

        dock_widget = QWidget()
        dock_widget.setLayout(menu_layout)
        self.dock.setWidget(dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.dock.hide()

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if self.folder_path:
            self.file_list.clear()
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".md"):
                    item = QListWidgetItem(filename)
                    icon_path = r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\icon_file.png"
                    icon = QIcon(icon_path)
                    item.setIcon(icon)
                    self.file_list.addItem(item)

            self.file_list.itemDoubleClicked.connect(self.open_file_from_list)
            self.file_list.show()
            self.dock.show()

    def open_file_from_list(self, item):
        file_path = os.path.join(self.folder_path, item.text())
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    note_content = file.read()
                note_name = os.path.basename(file_path)
                self.create_note_editor(note_name, note_content)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível abrir o arquivo: {str(e)}")

    def toggle_menu(self):
        if self.dock.width() > 50:
            self.dock.setFixedWidth(50)
            self.file_list.hide()
        else:
            self.dock.setFixedWidth(200)
            self.file_list.show()

    def add_new_note(self):
        note_name, ok = QInputDialog.getText(self, "Nome da Nota", "Digite o nome da nota:")
        if ok and note_name:
            self.create_note_editor(note_name)
        elif not ok:
            QMessageBox.warning(self, "Nenhum nome inserido", "Você não digitou nada.")

    def create_note_editor(self, note_name, content=""):
        try:
            note_editor = NoteEditor(self, note_name)
            note_editor.set_note_content(content)
            self.tab_widget.addTab(note_editor, note_name)
            self.tab_widget.setTabsClosable(True)
            self.tab_widget.tabCloseRequested.connect(self.close_tab)
            self.tab_widget.setCurrentWidget(note_editor)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao abrir a nota: {str(e)}")

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def save_current_note(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            note_editor = self.tab_widget.currentWidget()
            note_content = note_editor.get_note_content()

            if note_content:
                note_name = self.tab_widget.tabText(current_index)
                if note_name.endswith(".md"):
                    note_name = note_name[:-3]

                if hasattr(self, 'folder_path') and self.folder_path:
                    file_path = os.path.join(self.folder_path, f"{note_name}.md")
                else:
                    file_path, _ = QFileDialog.getSaveFileName(
                        self, "Salvar Nota", f"{note_name}", "Markdown Files (*.md);;All Files (*)"
                    )

                    if file_path and not file_path.endswith(".md"):
                        file_path += ".md"

                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(note_content)

                    QMessageBox.information(self, "Nota Salva", f"Sua nota '{note_name}' foi salva em {file_path}")

                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Não foi possível salvar o arquivo: {str(e)}")

    def open_existing_note(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Nota", "", "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    note_content = file.read()

                note_name = os.path.basename(file_path)
                self.create_note_editor(note_name, note_content)

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível abrir o arquivo: {str(e)}")
