import sys
from PyQt5.QtWidgets import QApplication
from views.noteView import NoteView

def main():
    app = QApplication(sys.argv)
    window = NoteView()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
