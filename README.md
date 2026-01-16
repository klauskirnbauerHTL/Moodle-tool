# 🎓 Moodle MCQ Tool

Ein benutzerfreundliches Desktop-Tool zum Erstellen, Verwalten und Exportieren von Multiple-Choice-Fragen für Moodle.

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 📝 **Fragen erstellen und bearbeiten** - Intuitive Oberfläche zum Erstellen von MC-Fragen
- 🏷️ **Tag-System** - Organisieren Sie Fragen mit bis zu 5 Tags
- 🔍 **Live-Suche** - Durchsuchen Sie Fragen nach Titel, Tags oder Fragetext
- 💾 **SQLite Datenbank** - Lokale Speicherung aller Fragen
- 📤 **Moodle XML Export** - Direkter Export für Moodle-Import
- 📄 **Word Export** - Exportieren Sie Fragen als professionelles 2-spaltiges Word-Dokument
- ⚡ **Single/Multiple Choice** - Unterstützung für beide Fragetypen
- 🖥️ **Vollbild-Optimiert** - Perfektes Layout auch im Vollbildmodus

## 🚀 Installation

### Voraussetzungen
- Python 3.9 oder höher
- PyQt6

### Installation
```bash
pip install PyQt6 python-docx
```

### Programm starten
```bash
python main.py
```

## 📦 Vorkompilierte Downloads

Für Windows und macOS stehen vorkompilierte ausführbare Dateien zur Verfügung:

👉 [Releases herunterladen](https://github.com/klauskirnbauerHTL/moodle-tool/releases)

- **macOS**: `.zip` mit Binary (siehe macOS Sicherheitshinweis unten)
- **Windows**: `.exe` Datei

### ⚠️ macOS Sicherheitshinweis

Da die App nicht von Apple signiert ist, müssen Sie beim ersten Start:

**Variante 1 - Rechtsklick:**
1. Rechtsklick (oder Ctrl+Klick) auf `MoodleTool`
2. "Öffnen" wählen
3. Im Dialog "Öffnen" bestätigen

**Variante 2 - Terminal:**
```bash
xattr -cr MoodleTool
./MoodleTool
```

**Variante 3 - Systemeinstellungen:**
1. Versuchen Sie die App zu öffnen
2. Systemeinstellungen → Datenschutz & Sicherheit
3. "Trotzdem öffnen" klicken

## 🎯 Verwendung

### Neue Frage erstellen
1. Klicken Sie auf "➕ Neue Frage"
2. Füllen Sie Titel, Fragetext und Punkte aus
3. Fügen Sie bis zu 5 Tags hinzu
4. Erstellen Sie bis zu 5 Antwortmöglichkeiten
5. Markieren Sie die richtigen Antworten
6. Klicken Sie auf "💾 FRAGE SPEICHERN"

### Fragen bearbeiten
- Doppelklicken Sie auf eine Frage in der Tabelle

### Fragen löschen
- Wählen Sie eine oder mehrere Fragen aus
- Klicken Sie auf "🗑️ Ausgewählte löschen"

### Moodle XML exportieren
1. Wählen Sie eine oder mehrere Fragen aus
2. Klicken Sie auf "📤 moodle.xml exportieren"
3. Wählen Sie einen Speicherort
4. Importieren Sie die XML-Datei in Moodle

### Word-Dokument exportieren (NEU! 🎉)
1. Wählen Sie eine oder mehrere Fragen aus
2. Klicken Sie auf "📄 Word exportieren"
3. Wählen Sie einen Speicherort
4. Das Word-Dokument wird mit 2-spaltigem Layout erstellt:
   - Professionelles Layout mit Checkboxen
   - Jede Frage auf einer Seite
   - Richtige Antworten sind grün markiert (zur Kontrolle)
   - Tags und Punkteanzahl sind enthalten
   - Kann direkt in Word, LibreOffice oder Google Docs geöffnet werden

### Suche verwenden
- Geben Sie Text in die Suchleiste ein
- Die Tabelle filtert automatisch nach Titel, Tags und Fragetext

## 🗂️ Datenbankstruktur

Das Tool verwendet eine SQLite-Datenbank (`mcq_questions.db`) mit folgenden Tabellen:

### Tabelle: questions
- `id` - Eindeutige ID
- `title` - Fragentitel
- `questiontext` - Fragetext (HTML möglich)
- `single` - Single Choice (1) oder Multiple Choice (0)
- `tags` - Komma-getrennte Tags
- `points` - Punkte für die Frage

### Tabelle: answers
- `id` - Eindeutige ID
- `question_id` - Referenz zur Frage
- `answertext` - Antworttext
- `is_correct` - Richtig (1) oder Falsch (0)

## 🛠️ Entwicklung

### Projekt-Struktur
```
moodle-tool/
├── main.py              # Einstiegspunkt
├── main_window.py       # Hauptfenster
├── dialogs.py           # Dialoge (Frage bearbeiten, Einstellungen)
├── database.py          # Datenbankoperationen
├── exporter.py          # Moodle XML Export
├── .github/workflows/   # CI/CD Pipeline
└── MoodleTool.spec      # PyInstaller Konfiguration
```

### CI/CD Pipeline
Das Projekt verwendet GitHub Actions für automatisches Testen und Builds:
- Tests auf Ubuntu, macOS und Windows
- Automatische Erstellung von `.app` und `.exe` Dateien
- Release-Management bei Git Tags

Mehr Details: [CI-CD-README.md](CI-CD-README.md)

### Eigene Builds erstellen
```bash
pip install pyinstaller
pyinstaller MoodleTool.spec
```

## 📝 Changelog

### Version 2.7 (16. Januar 2026)
- ✨ **NEU**: Frage duplizieren Funktion
- 📋 Button und Menüoption (Ctrl+D) zum Duplizieren von Fragen
- 🔧 Automatische Markierung mit "(Kopie)" im Titel
- 📦 Python Virtual Environment Setup mit requirements.txt
- 📚 Dokumentation für Virtual Environment (README_VENV.md)

### Version 1.1.0 (18. Dezember 2025)
- ✨ **NEU**: Word-Export Funktion mit 2-spaltigem Layout
- 📄 Professionelle Word-Dokumente mit Checkboxen für Antworten
- 🎨 Farbige Markierung richtiger Antworten (grün) zur Kontrolle
- 📋 Übersichtliche Formatierung mit Titel, Punkten und Tags
- 🔧 python-docx Dependency hinzugefügt

### Version 1.0.0 (6. Dezember 2025)
- ✅ Vollbild-optimiertes Layout mit ScrollArea
- ✅ CI/CD Pipeline für Windows und macOS
- ✅ Verbesserte Tag-Verwaltung
- ✅ Live-Suche über alle Felder
- ✅ Löschen von mehreren Fragen

## 🤝 Beitragen

Contributions sind willkommen! Bitte:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature Branch
3. Committen Sie Ihre Änderungen
4. Pushen Sie zum Branch
5. Öffnen Sie einen Pull Request

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 👨‍💻 Autor

**Klaus Kirnbauer**
- HTL Pinkafeld

## 🐛 Bugs melden

Bitte öffnen Sie ein [Issue](https://github.com/klauskirnbauerHTL/moodle-tool/issues) auf GitHub.

## 💡 Feature-Anfragen

Feature-Vorschläge können ebenfalls als [Issue](https://github.com/klauskirnbauerHTL/moodle-tool/issues) eingereicht werden.

---

**Viel Erfolg beim Erstellen Ihrer Moodle-Fragen! 🎓**
