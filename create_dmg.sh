#!/bin/bash
# DMG Creator für MoodleTool
# Erstellt eine professionelle DMG-Datei mit Drag&Drop Installation

echo "🔨 Erstelle DMG für MoodleTool..."

# Prüfe ob die App existiert
if [ ! -d "dist/MoodleTool.app" ]; then
    echo "❌ Fehler: dist/MoodleTool.app nicht gefunden!"
    echo "   Bitte erst 'pyinstaller MoodleTool.spec' ausführen"
    exit 1
fi

# Erstelle temporären Ordner für DMG-Inhalt
echo "📁 Erstelle DMG-Struktur..."
rm -rf dist/dmg_temp
mkdir -p dist/dmg_temp

# Kopiere die App
echo "📦 Kopiere MoodleTool.app..."
cp -r dist/MoodleTool.app dist/dmg_temp/

# Erstelle Symlink zu Applications für Drag&Drop
echo "🔗 Erstelle Applications-Link..."
ln -s /Applications dist/dmg_temp/Applications

# Erstelle DMG
echo "💾 Erstelle DMG-Datei..."
hdiutil create \
    -volname "Moodle MCQ Tool" \
    -srcfolder dist/dmg_temp \
    -ov \
    -format UDZO \
    dist/MoodleTool.dmg

# Aufräumen
echo "🧹 Räume auf..."
rm -rf dist/dmg_temp

if [ -f "dist/MoodleTool.dmg" ]; then
    echo "✅ DMG erfolgreich erstellt: dist/MoodleTool.dmg"
    echo ""
    echo "📊 Dateigröße:"
    ls -lh dist/MoodleTool.dmg
    echo ""
    echo "🚀 Zum Installieren:"
    echo "   1. Öffne MoodleTool.dmg"
    echo "   2. Ziehe MoodleTool.app in den Applications Ordner"
else
    echo "❌ Fehler beim Erstellen der DMG!"
    exit 1
fi
