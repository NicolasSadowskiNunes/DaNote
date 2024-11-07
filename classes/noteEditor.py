from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QSizePolicy
from PyQt5.QtGui import QTextCharFormat, QFont, QIcon
from PyQt5.QtCore import QSize
import markdown

class NoteEditor(QWidget):
    def __init__(self, parent=None, note_name="Nota"):
        super().__init__(parent)

        # Área de texto para o usuário editar
        self.text_edit = QTextEdit(self)

        # Seletor do tamanho da fonte
        self.font_size_selector = QComboBox(self)
        self.font_size_selector.addItems([str(i) for i in range(8, 32)])  # Tamanhos de 8 a 30
        self.font_size_selector.currentIndexChanged.connect(self.update_text_format)
        self.font_size_selector.setFixedSize(QSize(200, 25))

        # Botões de negrito, itálico e sublinhado
        self.bold_button = self.create_format_button("icon_bold.png")
        self.italic_button = self.create_format_button("icon_italic.png")
        self.underline_button = self.create_format_button("icon_underline.png")

        # Layout de formatação
        format_layout = QHBoxLayout()
        format_layout.addWidget(self.font_size_selector)
        format_layout.addWidget(self.bold_button)
        format_layout.addWidget(self.italic_button)
        format_layout.addWidget(self.underline_button)
        format_layout.addStretch()

        # Layout principal
        layout = QVBoxLayout()
        layout.addLayout(format_layout)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.update_text_format()

    def create_format_button(self, icon_name):
        button = QPushButton(self)
        button.setCheckable(True)
        button.setIcon(QIcon(r"C:\Users\nicol\PycharmProjects\NoteAnoted\assets\\" + icon_name))
        button.clicked.connect(self.update_text_format)
        button.setFixedSize(QSize(40, 30))
        return button

    def update_text_format(self):
        text_format = QTextCharFormat()
        text_format.setFontPointSize(int(self.font_size_selector.currentText()))
        text_format.setFontWeight(QFont.Bold if self.bold_button.isChecked() else QFont.Normal)
        text_format.setFontItalic(self.italic_button.isChecked())
        text_format.setFontUnderline(self.underline_button.isChecked())
        self.text_edit.setCurrentCharFormat(text_format)

    def get_note_content(self):
        
        return self.convert_to_markdown(self.text_edit.toHtml())

    def set_note_content(self, content):
       
        html_content = self.convert_markdown_to_html(content)
        self.text_edit.setHtml(html_content)

    def convert_to_markdown(self, html_content):
        """Converte o conteúdo HTML em Markdown."""
        return markdown.markdown(html_content)

    def convert_markdown_to_html(self, markdown_content):
        """Converte o conteúdo Markdown para HTML."""
        return markdown.markdown(markdown_content)
