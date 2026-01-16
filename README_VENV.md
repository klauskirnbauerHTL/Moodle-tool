# Python Virtual Environment Setup

## Virtual Environment erstellen und aktivieren

### macOS/Linux:
```bash
# Virtual Environment erstellen
python3 -m venv venv

# Virtual Environment aktivieren
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### Windows:
```bash
# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

## Anwendung starten

Nach Aktivierung des Virtual Environments:
```bash
python main.py
```

## Virtual Environment deaktivieren

```bash
deactivate
```

## Installierte Packages

Die folgenden Packages sind in der `requirements.txt` aufgelistet:
- **PyQt6** (6.10.2) - GUI Framework
- **python-docx** (1.2.0) - Word-Export
- **pyinstaller** (6.18.0) - Build für ausführbare Dateien

## Hinweise

- Das `venv/` Verzeichnis wird nicht ins Git-Repository committed (siehe `.gitignore`)
- Bei Änderungen an Dependencies: `pip freeze > requirements.txt` ausführen
