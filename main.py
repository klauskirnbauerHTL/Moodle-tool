import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from main_window import MainWindow
import os
from database import init_database_schema

def select_database_at_start():
    app = QApplication(sys.argv)
    
    # DB-Auswahl zu Programmstart:
    filename, _ = QFileDialog.getOpenFileName(
        None,
        "SQLite Datenbank wählen oder neu erstellen",
        os.getcwd(),
        "SQLite DB (*.db)"
    )
    
    if not filename:
        # Verhindert Start ohne DB-Auswahl
        QMessageBox.warning(None, "Keine DB gewählt", "Es wurde keine Datenbank ausgewählt. Das Programm wird beendet.")
        sys.exit(0)
    
    # Neue DB ggf. anlegen (wenn File nicht existiert)
    if not os.path.exists(filename):
        # Lege DB mit Schema an
        init_database_schema(filename)
    
    # Hauptfenster mit gewählter DB starten
    window = MainWindow(db_path=filename)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    select_database_at_start()