import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFileDialog, QLineEdit, QLabel
)
from PyQt6.QtGui import QKeySequence, QAction
from PyQt6.QtCore import Qt
import sqlite3

from dialogs import QuestionDialog, SettingsDialog
from exporter import export_to_moodle_xml
from database import init_database_schema, get_questions_overview, import_moodle_xml


class MainWindow(QMainWindow):
    def __init__(self, db_path="mcq_questions.db"):
        super().__init__()
        self.db_path = db_path
        self.init_db()

        # 🖥️ VOLLBILD AUTOMATISCH
        self.setWindowState(Qt.WindowState.WindowMaximized)
        
        self.setWindowTitle("Moodle MCQ Tool v2.5")
        self.create_menu()
        self.setup_central_widget()
        self.refresh_table()

    def setup_central_widget(self):
        central = QWidget()
        layout = QVBoxLayout()

        # 🔍 Suchleiste (volle Breite)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Suche (live):"))
        self.search_edit = QLineEdit()
        self.search_edit.setMinimumHeight(40)
        self.search_edit.setPlaceholderText("Titel, Tags oder Fragetext eingeben...")
        self.search_edit.textChanged.connect(self.apply_filter)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)

        # 6-Spalten-Tabelle MIT FRAGETEXT
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Titel", "Punkte", "Tags", "Antworten", "Fragetext (Vorschau)"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # SPALTENBREITEN OPTIMAL
        self.table.setColumnWidth(0, 60)   # ID
        self.table.setColumnWidth(1, 250)  # Titel
        self.table.setColumnWidth(2, 80)   # Punkte
        self.table.setColumnWidth(3, 220)  # Tags
        self.table.setColumnWidth(4, 90)   # Antworten
        self.table.setColumnWidth(5, 400)  # Fragetext
        
        self.table.cellDoubleClicked.connect(self.edit_question)
        layout.addWidget(self.table)

        # BUTTONS mit LÖSCHEN (volle Breite)
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("➕ Neue Frage")
        new_btn.setMinimumHeight(45)
        new_btn.clicked.connect(self.new_question)

        refresh_btn = QPushButton("🔄 Alle anzeigen")
        refresh_btn.setMinimumHeight(45)
        refresh_btn.clicked.connect(self.refresh_table)

        # LÖSCHEN BUTTON
        delete_btn = QPushButton("🗑️ Ausgewählte löschen")
        delete_btn.setMinimumHeight(45)
        delete_btn.clicked.connect(self.delete_selected_questions)
        
        export_btn = QPushButton("📤 moodle.xml exportieren")
        export_btn.setMinimumHeight(45)
        export_btn.clicked.connect(self.export_xml)

        button_layout.addWidget(new_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(export_btn)
        layout.addLayout(button_layout)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # Daten für Filterung
        self.all_rows = []
        self.all_question_texts = {}

    def create_menu(self):
        menubar = self.menuBar()
        
        # Einstellungen
        settings_menu = menubar.addMenu("Einstellungen")
        settings_action = QAction("Datenbank...", self)
        settings_action.setShortcut(QKeySequence("Ctrl+D"))
        settings_action.triggered.connect(self.show_settings)
        settings_menu.addAction(settings_action)
        
        # LÖSCHEN im Menü
        delete_menu = menubar.addMenu("Bearbeiten")
        delete_action = QAction("🗑️ Ausgewählte löschen", self)
        delete_action.setShortcut(QKeySequence("Ctrl+Delete"))
        delete_action.triggered.connect(self.delete_selected_questions)
        delete_menu.addAction(delete_action)
        
        # Import
        import_menu = menubar.addMenu("Import")
        import_action = QAction("Moodle XML importieren...", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(self.import_moodle_xml)
        import_menu.addAction(import_action)

    def delete_selected_questions(self):
        """🗑️ LÖSCHT markierte Fragen mit Sicherheitsabfrage"""
        selected_rows = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item and self.table.item(i, 0).isSelected():
                selected_rows.append(i)

        if not selected_rows:
            QMessageBox.warning(self, "⚠️ Keine Auswahl", "Wähle mindestens eine Frage aus!")
            return

        # TITEL der zu löschenden Fragen sammeln
        questions_to_delete = []
        for row in selected_rows:
            qid = int(self.table.item(row, 0).text())
            title = self.table.item(row, 1).text()
            questions_to_delete.append(f"• {title} (ID: {qid})")

        # SICHERHEITSABFRAGE mit Liste
        delete_text = f"Sollen {len(questions_to_delete)} Frage(n) GELÖSCHT werden?\n\n"
        delete_text += "💥 **ACHTUNG: Dieser Vorgang kann NICHT rückgängig gemacht werden!**\n\n"
        delete_text += "Zu löschende Fragen:\n" + "\n".join(questions_to_delete[:5])
        if len(questions_to_delete) > 5:
            delete_text += f"\n... und {len(questions_to_delete)-5} weitere"

        reply = QMessageBox.critical(
            self,
            f"🗑️ {len(questions_to_delete)} Frage(n) löschen?",
            delete_text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return

        # LÖSCHEN
        question_ids = [int(self.table.item(row, 0).text()) for row in selected_rows]
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            for qid in question_ids:
                c.execute("DELETE FROM questions WHERE id=?", (qid,))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "✅ Gelöscht", f"🗑️ {len(question_ids)} Frage(n) erfolgreich gelöscht!")
            self.refresh_table()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Löschfehler", f"Konnte Fragen nicht löschen:\n{str(e)}")

    def show_settings(self):
        dialog = SettingsDialog(self.db_path, self)
        result = dialog.exec()
        if result == dialog.DialogCode.Accepted:
            new_db_text = dialog.new_db_path.text()
            if new_db_text != "Keine ausgewählt":
                self.db_path = new_db_text
                init_database_schema(self.db_path)
                self.setWindowTitle(f"Moodle MCQ Tool v2.5 - DB: {os.path.basename(self.db_path)}")
                self.refresh_table()

    def import_moodle_xml(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Moodle XML importieren", "", "Moodle XML (*.xml)")
        if not filename:
            return
        imported_count, message = import_moodle_xml(self.db_path, filename)
        QMessageBox.information(self, "Import abgeschlossen", message)
        self.refresh_table()

    def init_db(self):
        init_database_schema(self.db_path)

    def new_question(self):
        dialog = QuestionDialog(self.db_path, parent=self)
        if dialog.exec():
            self.refresh_table()

    def edit_question(self, row, column):
        item = self.table.item(row, 0)
        if not item:
            return
        question_id = int(item.text())
        dialog = QuestionDialog(self.db_path, question_id=question_id, parent=self)
        if dialog.exec():
            self.refresh_table()

    def refresh_table(self):
        """Lädt ALLE Fragen inkl. Fragetext-Cache"""
        try:
            self.all_rows = get_questions_overview(self.db_path)
            
            # Fragetext-Cache füllen
            self.all_question_texts.clear()
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            for row in self.all_rows:
                qid = row[0]
                c.execute("SELECT questiontext FROM questions WHERE id=?", (qid,))
                result = c.fetchone()
                self.all_question_texts[qid] = result[0] if result else ""
            conn.close()
            
            self.apply_filter()
            status = f"Alle Fragen geladen: {len(self.all_rows)}"
            self.statusBar().showMessage(status)
        except Exception as e:
            QMessageBox.critical(self, "DB Fehler", f"Konnte DB nicht öffnen:\n{str(e)}")

    def apply_filter(self):
        """Filtert UND zeigt Tabelle mit Fragetext-Spalte"""
        try:
            search_term = self.search_edit.text().strip().lower()
            
            if not search_term:
                filtered_rows = self.all_rows
            else:
                filtered_rows = []
                for row in self.all_rows:
                    qid, title, points, tags, count = row
                    questiontext = self.all_question_texts.get(qid, "").lower()
                    search_text = f"{title.lower()} {tags.lower()} {questiontext}"
                    if search_term in search_text:
                        filtered_rows.append(row)

            # 6 SPALTEN FÜLLEN (mit Fragetext!)
            self.table.setRowCount(len(filtered_rows))
            for i, row in enumerate(filtered_rows):
                qid, title, points, tags, count = row
                question_preview = self.all_question_texts.get(qid, "")[:80] + "..." if len(self.all_question_texts.get(qid, "")) > 80 else self.all_question_texts.get(qid, "")
                
                self.table.setItem(i, 0, QTableWidgetItem(str(qid)))
                self.table.setItem(i, 1, QTableWidgetItem(title))
                self.table.setItem(i, 2, QTableWidgetItem(f"{points:.1f}"))
                tags_short = tags[:25] + "..." if len(tags) > 25 else tags
                self.table.setItem(i, 3, QTableWidgetItem(tags_short))
                self.table.setItem(i, 4, QTableWidgetItem(str(count)))
                self.table.setItem(i, 5, QTableWidgetItem(question_preview))

            total = len(self.all_rows)
            found = len(filtered_rows)
            status = f"Gefunden: {found} von {total} Fragen"
            self.statusBar().showMessage(status)

        except Exception as e:
            self.statusBar().showMessage(f"Filter Fehler: {str(e)}")

    def export_xml(self):
        selected_rows = set()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item and self.table.item(i, 0).isSelected():
                selected_rows.add(i)

        if not selected_rows:
            QMessageBox.warning(self, "Fehler", "Wähle mindestens eine Frage aus!")
            return

        question_ids = [int(self.table.item(row, 0).text()) for row in selected_rows]
        filename, _ = QFileDialog.getSaveFileName(self, "moodle.xml speichern", "moodle_quiz.xml", "XML (*.xml)")
        if filename:
            try:
                export_to_moodle_xml(self.db_path, question_ids, filename)
                QMessageBox.information(self, "Erfolg", f"{len(question_ids)} Fragen exportiert!\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Export fehlgeschlagen:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
