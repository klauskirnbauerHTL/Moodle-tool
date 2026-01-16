import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton
from main_window import MainWindow
import os
from database import init_database_schema

def select_database_at_start():
    app = QApplication(sys.argv)
    
    # Dialog mit Optionen anzeigen
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setWindowTitle("Datenbank auswählen")
    msg.setText("Möchtest du eine bestehende Datenbank öffnen oder eine neue erstellen?")
    
    # Buttons für die Optionen
    btn_open = msg.addButton("📂 Bestehende öffnen", QMessageBox.ButtonRole.AcceptRole)
    btn_new = msg.addButton("➕ Neue erstellen", QMessageBox.ButtonRole.AcceptRole)
    btn_cancel = msg.addButton("❌ Abbrechen", QMessageBox.ButtonRole.RejectRole)
    
    msg.exec()
    clicked = msg.clickedButton()
    
    filename = None
    
    if clicked == btn_cancel:
        sys.exit(0)
    elif clicked == btn_open:
        # Bestehende DB öffnen
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "SQLite Datenbank auswählen",
            os.getcwd(),
            "SQLite DB (*.db)"
        )
    elif clicked == btn_new:
        # Neue DB erstellen
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Neue SQLite Datenbank erstellen",
            os.path.join(os.getcwd(), "moodle_questions.db"),
            "SQLite DB (*.db)"
        )
        if filename and not filename.endswith('.db'):
            filename += '.db'
    
    if not filename:
        # Verhindert Start ohne DB-Auswahl
        QMessageBox.warning(None, "Keine DB gewählt", "Es wurde keine Datenbank ausgewählt. Das Programm wird beendet.")
        sys.exit(0)
    
    # Neue DB ggf. anlegen (wenn File nicht existiert)
    if not os.path.exists(filename):
        # Lege DB mit Schema an
        init_database_schema(filename)
        QMessageBox.information(None, "✅ Datenbank erstellt", f"Neue Datenbank wurde erfolgreich erstellt:\n{os.path.basename(filename)}")
    
    # Hauptfenster mit gewählter DB starten
    window = MainWindow(db_path=filename)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    select_database_at_start()