# Moodle MCQ Tool - CI/CD Pipeline

Diese Anwendung verwendet GitHub Actions für automatisches Testen und Erstellen von ausführbaren Dateien.

## 📋 Was macht die Pipeline?

### 1. **Test Job**
- Testet die Anwendung auf Ubuntu, macOS und Windows
- Prüft Python-Versionen 3.9, 3.10 und 3.11
- Installiert alle Abhängigkeiten
- Überprüft die Syntax aller Python-Dateien

### 2. **Build Job**
- Erstellt ausführbare Dateien für macOS und Windows
- Verwendet PyInstaller für das Packaging
- **macOS**: Erstellt `.app` Bundle und optional `.dmg` Installer
- **Windows**: Erstellt `.exe` Datei

### 3. **Artifacts**
- Hochladen der Build-Artefakte für 30 Tage
- Bei Tagged Releases: Automatisches Erstellen eines GitHub Release

## 🚀 Verwendung

### Automatische Builds
Die Pipeline läuft automatisch bei:
- Push auf `main` oder `V1.0` Branch
- Pull Requests
- Manueller Trigger über GitHub UI

### Release erstellen
1. Erstellen Sie einen Git Tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Die Pipeline erstellt automatisch ein GitHub Release mit den Build-Dateien

### Manuelle Builds lokal

#### macOS
```bash
pip install PyQt6 pyinstaller
pyinstaller --name="MoodleTool" --windowed --onefile main.py
```

#### Windows
```bash
pip install PyQt6 pyinstaller
pyinstaller --name="MoodleTool" --windowed --onefile main.py
```

#### Mit Spec-Datei (erweiterte Konfiguration)
```bash
pyinstaller MoodleTool.spec
```

## 📦 Output

### macOS
- `moodle-tool-macos.zip` - Komprimierte .app Datei
- `moodle-tool-macos.dmg` - DMG Installer (optional)

### Windows
- `moodle-tool-windows.zip` - Komprimierte .exe Datei

## 🔧 Anpassungen

### Icon hinzufügen
1. Erstellen Sie `icon.icns` (macOS) und `icon.ico` (Windows)
2. Die Pipeline verwendet diese automatisch

### Weitere Abhängigkeiten
Fügen Sie diese in `.github/workflows/build-and-release.yml` hinzu:
```yaml
- name: Install dependencies
  run: |
    pip install PyQt6 pyinstaller ihre-weitere-abhängigkeit
```

## 🐛 Troubleshooting

### PyInstaller findet Module nicht
Fügen Sie Hidden Imports in `MoodleTool.spec` hinzu:
```python
hiddenimports=['module_name']
```

### macOS Gatekeeper Probleme
Signieren Sie die App:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID" MoodleTool.app
```

### Windows Antivirus False Positives
Verwenden Sie Code-Signing mit einem Zertifikat

## 📝 Weitere Informationen

- [GitHub Actions Dokumentation](https://docs.github.com/en/actions)
- [PyInstaller Dokumentation](https://pyinstaller.org/)
