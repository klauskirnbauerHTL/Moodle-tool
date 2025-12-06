import os
import sqlite3
from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QCheckBox,
    QDoubleSpinBox, QPushButton, QMessageBox, QFileDialog,
    QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QWidget
)
from PyQt6.QtCore import Qt


class QuestionDialog(QDialog):
    def __init__(self, db_path, question_id=None, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.question_id = question_id
        self.setWindowTitle("Frage bearbeiten" if question_id else "Neue MC-Frage erstellen")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setup_ui()
        if self.question_id:
            self.load_question()

    def setup_ui(self):
        # Hauptcontainer für ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # TITEL
        title_layout = QVBoxLayout()
        title_label = QLabel("📝 Titel:")
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 5px;")
        title_layout.addWidget(title_label)
        self.title_edit = QLineEdit()
        self.title_edit.setMinimumHeight(50)
        self.title_edit.setMaximumHeight(60)
        self.title_edit.setStyleSheet("padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px;")
        self.title_edit.setPlaceholderText("Fragentitel hier eingeben...")
        title_layout.addWidget(self.title_edit)
        main_layout.addLayout(title_layout)

        # FRAGETEXT
        question_layout = QVBoxLayout()
        question_label = QLabel("❓ Fragetext:")
        question_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        question_layout.addWidget(question_label)
        self.question_edit = QTextEdit()
        self.question_edit.setMinimumHeight(180)
        self.question_edit.setMaximumHeight(250)
        self.question_edit.setStyleSheet("font-size: 15px; padding: 12px; border: 2px solid #ddd; border-radius: 8px;")
        self.question_edit.setPlaceholderText("Fragetext hier eingeben (HTML möglich)...")
        question_layout.addWidget(self.question_edit)
        main_layout.addLayout(question_layout)

        # PUNKTE + SINGLE CHOICE
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        points_label = QLabel("⭐ Punkte:")
        points_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        options_layout.addWidget(points_label)
        
        self.points_spin = QDoubleSpinBox()
        self.points_spin.setRange(0.1, 10.0)
        self.points_spin.setValue(1.0)
        self.points_spin.setDecimals(1)
        self.points_spin.setMinimumHeight(40)
        self.points_spin.setMaximumHeight(50)
        self.points_spin.setMaximumWidth(120)
        self.points_spin.setStyleSheet("padding: 8px; font-size: 15px;")
        options_layout.addWidget(self.points_spin)
        
        options_layout.addSpacing(30)
        
        self.single_cb = QCheckBox("⚡ Single Choice (nicht Multiple)")
        self.single_cb.setChecked(True)
        self.single_cb.setStyleSheet("font-size: 15px; padding: 8px;")
        options_layout.addWidget(self.single_cb)
        
        options_layout.addStretch()
        main_layout.addLayout(options_layout)

        # 5 TAG-FELDER "Tag 1" bis "Tag 5"
        tags_title = QLabel("🏷️  Tags:")
        tags_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px; margin-bottom: 8px;")
        main_layout.addWidget(tags_title)
        
        tags_layout = QGridLayout()
        tags_layout.setSpacing(12)
        tags_layout.setHorizontalSpacing(25)
        
        self.tag_edits = []
        for i in range(5):
            tag_label = QLabel(f"Tag {i+1}:")
            tag_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            tag_label.setMinimumWidth(60)
            tag_label.setMaximumWidth(80)
            tag_edit = QLineEdit()
            tag_edit.setMinimumHeight(40)
            tag_edit.setMaximumHeight(50)
            tag_edit.setStyleSheet("padding: 10px; font-size: 14px; border: 2px solid #ddd; border-radius: 6px;")
            tag_edit.setPlaceholderText(f"Tag {i+1} eingeben...")
            tags_layout.addWidget(tag_label, i, 0)
            tags_layout.addWidget(tag_edit, i, 1)
            self.tag_edits.append(tag_edit)
        
        main_layout.addLayout(tags_layout)

        # ANTWORTEN
        answers_title = QLabel("💬 Antworten:")
        answers_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px; margin-bottom: 8px;")
        main_layout.addWidget(answers_title)
        
        self.answers = []
        for i in range(5):
            # Vertikales Layout für jede Antwort
            answer_container = QVBoxLayout()
            answer_container.setSpacing(5)
            
            # Label und Checkbox in einer Zeile
            header_layout = QHBoxLayout()
            answer_label = QLabel(f"Antwort {i+1}:")
            answer_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            header_layout.addWidget(answer_label)
            
            correct_cb = QCheckBox("✅ Richtig")
            correct_cb.setStyleSheet("font-size: 14px; padding: 5px;")
            header_layout.addWidget(correct_cb)
            header_layout.addStretch()
            
            answer_container.addLayout(header_layout)
            
            # Textfeld darunter
            answer_edit = QTextEdit()
            answer_edit.setMinimumHeight(100)
            answer_edit.setMaximumHeight(150)
            answer_edit.setStyleSheet("font-size: 14px; padding: 10px; border: 2px solid #ddd; border-radius: 8px;")
            answer_edit.setPlaceholderText(f"Antwort {i+1} hier eingeben (mehrzeilig, HTML möglich)...")
            answer_container.addWidget(answer_edit)
            
            main_layout.addLayout(answer_container)
            self.answers.extend([answer_edit, correct_cb])

        # SPEICHERN BUTTON
        main_layout.addSpacing(20)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        save_btn = QPushButton("💾 FRAGE SPEICHERN")
        save_btn.setMinimumHeight(55)
        save_btn.setMaximumHeight(65)
        save_btn.setMinimumWidth(280)
        save_btn.setMaximumWidth(400)
        save_btn.setStyleSheet("""
            QPushButton { 
                font-weight: bold; 
                font-size: 16px; 
                padding: 12px 35px; 
                background-color: #4CAF50; 
                color: white; 
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { 
                background-color: #45a049; 
            }
            QPushButton:pressed { 
                background-color: #3d8b40; 
            }
        """)
        save_btn.clicked.connect(self.save_question)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # ScrollArea als Hauptlayout setzen
        scroll_area.setWidget(scroll_widget)
        dialog_layout = QVBoxLayout()
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(scroll_area)
        self.setLayout(dialog_layout)

    def get_tags_string(self):
        tags = []
        for tag_edit in self.tag_edits:
            tag_text = tag_edit.text().strip()
            if tag_text:
                tags.append(tag_text)
        return ",".join(tags)

    def load_question(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT title, questiontext, single, tags, points FROM questions WHERE id=?", (self.question_id,))
        row = c.fetchone()
        if not row:
            conn.close()
            return
        self.title_edit.setText(row[0])
        self.question_edit.setPlainText(row[1])
        self.single_cb.setChecked(row[2] == 1)
        self.points_spin.setValue(row[4])
        
        tags_str = row[3]
        if tags_str:
            tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
            for i, tag_edit in enumerate(self.tag_edits):
                if i < len(tag_list):
                    tag_edit.setText(tag_list[i])
        
        c.execute("SELECT answertext, is_correct FROM answers WHERE question_id=? ORDER BY id", (self.question_id,))
        answers = c.fetchall()
        for i, (answer_text, is_correct) in enumerate(answers):
            if i * 2 < len(self.answers):
                self.answers[2 * i].setPlainText(answer_text)
                self.answers[2 * i + 1].setChecked(is_correct == 1)
        conn.close()

    def save_question(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Fehler", "Titel erforderlich!")
            return
        
        answers = []
        for i in range(0, len(self.answers), 2):
            answer_text = self.answers[i].toPlainText()
            is_correct = 1 if self.answers[i + 1].isChecked() else 0
            answers.append((answer_text, is_correct))
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        tags = self.get_tags_string()
        
        if self.question_id:
            c.execute(
                """UPDATE questions SET title=?, questiontext=?, single=?, tags=?, points=? WHERE id=?""",
                (self.title_edit.text().strip(), self.question_edit.toPlainText().strip(),
                 1 if self.single_cb.isChecked() else 0, tags, self.points_spin.value(), self.question_id)
            )
            c.execute("DELETE FROM answers WHERE question_id=?", (self.question_id,))
            qid = self.question_id
        else:
            c.execute(
                "INSERT INTO questions (title, questiontext, single, tags, points) VALUES (?, ?, ?, ?, ?)",
                (self.title_edit.text().strip(), self.question_edit.toPlainText().strip(),
                 1 if self.single_cb.isChecked() else 0, tags, self.points_spin.value())
            )
            qid = c.lastrowid
        
        for answer_text, is_correct in answers:
            if answer_text.strip():
                c.execute("INSERT INTO answers (question_id, answertext, is_correct) VALUES (?, ?, ?)",
                         (qid, answer_text.strip(), is_correct))
        
        conn.commit()
        conn.close()
        QMessageBox.information(self, "✅ Erfolg", "Frage gespeichert!")
        self.accept()


class SettingsDialog(QDialog):
    def __init__(self, current_db_path, parent=None):
        super().__init__(parent)
        self.current_db_path = current_db_path
        self.setWindowTitle("Datenbank Einstellungen")
        self.setMinimumWidth(600)
        layout = QVBoxLayout()
        current_label = QLabel(f"Aktuelle DB: {current_db_path or 'Keine'}")
        layout.addWidget(current_label)
        db_btn = QPushButton("Neue Datenbank auswählen...")
        db_btn.clicked.connect(self.select_new_db)
        layout.addWidget(db_btn)
        self.new_db_path = QLabel("Keine ausgewählt")
        layout.addWidget(self.new_db_path)
        layout.addWidget(QLabel("Bestehende .db Dateien im Ordner:"))
        self.db_list = QListWidget()
        self.refresh_db_list()
        layout.addWidget(self.db_list)
        btn_layout = QHBoxLayout()
        remove_btn = QPushButton("Ausgewählte DB entfernen")
        remove_btn.clicked.connect(self.remove_selected_db)
        apply_btn = QPushButton("Übernehmen")
        apply_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def refresh_db_list(self):
        self.db_list.clear()
        try:
            dir_path = os.path.dirname(self.current_db_path) if self.current_db_path else os.getcwd()
            for file in os.listdir(dir_path):
                if file.endswith(".db"):
                    size_kb = os.path.getsize(os.path.join(dir_path, file)) / 1024
                    item_text = f"{file} ({size_kb:.1f} KB)"
                    self.db_list.addItem(item_text)
        except Exception:
            pass

    def select_new_db(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Neue Datenbank erstellen", "", "SQLite DB (*.db)")
        if filename:
            self.new_db_path.setText(filename)

    def remove_selected_db(self):
        current_item = self.db_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Fehler", "Wähle eine DB aus!")
            return
        db_name = current_item.text().split(" ")[0]
        dir_path = os.path.dirname(self.current_db_path) if self.current_db_path else os.getcwd()
        db_path = os.path.join(dir_path, db_name)
        reply = QMessageBox.question(self, "Löschen bestätigen", f"Sollen '{db_name}' gelöscht werden?\n\nACHTUNG: Alle Fragen gehen verloren!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(db_path)
                QMessageBox.information(self, "Gelöscht", f"'{db_name}' entfernt!")
                self.refresh_db_list()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte nicht löschen:\n{str(e)}")
