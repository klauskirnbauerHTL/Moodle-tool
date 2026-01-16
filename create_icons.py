#!/usr/bin/env python3
"""
Icon Generator für MoodleTool
Erstellt Icons in verschiedenen Formaten aus icon.jpg
"""

from PIL import Image
import os

def create_icons():
    """Erstellt Icons für alle Plattformen"""
    
    # Lade das Original-Bild
    print("Lade icon.jpg...")
    img = Image.open('icon.jpg')
    
    # Konvertiere zu RGBA (für Transparenz-Unterstützung)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 1. Windows ICO (mehrere Größen)
    print("Erstelle icon.ico für Windows...")
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save('icon.ico', format='ICO', sizes=icon_sizes)
    print("✓ icon.ico erstellt")
    
    # 2. macOS ICNS - erstelle zuerst .iconset Ordner mit verschiedenen Größen
    print("Erstelle icon.icns für macOS...")
    iconset_dir = 'icon.iconset'
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # macOS benötigt spezifische Größen
    macos_sizes = [
        (16, 16, 'icon_16x16.png'),
        (32, 32, 'icon_16x16@2x.png'),
        (32, 32, 'icon_32x32.png'),
        (64, 64, 'icon_32x32@2x.png'),
        (128, 128, 'icon_128x128.png'),
        (256, 256, 'icon_128x128@2x.png'),
        (256, 256, 'icon_256x256.png'),
        (512, 512, 'icon_256x256@2x.png'),
        (512, 512, 'icon_512x512.png'),
        (1024, 1024, 'icon_512x512@2x.png'),
    ]
    
    for width, height, filename in macos_sizes:
        resized = img.resize((width, height), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_dir, filename))
    
    # Konvertiere .iconset zu .icns (nur auf macOS möglich)
    if os.system('which iconutil > /dev/null 2>&1') == 0:
        os.system('iconutil -c icns icon.iconset -o icon.icns')
        print("✓ icon.icns erstellt")
        # Aufräumen
        os.system('rm -rf icon.iconset')
    else:
        print("⚠️ iconutil nicht gefunden - icon.icns konnte nicht erstellt werden")
        print("   (Dies funktioniert nur auf macOS)")
    
    # 3. PNG für Linux/allgemein (verschiedene Größen)
    print("Erstelle PNG-Icons...")
    for size in [16, 32, 48, 64, 128, 256, 512]:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'icon_{size}x{size}.png')
    print("✓ PNG-Icons erstellt")
    
    print("\n✅ Alle Icons erfolgreich erstellt!")
    print("\nErstellt:")
    print("  - icon.ico (Windows)")
    print("  - icon.icns (macOS)")
    print("  - icon_*.png (verschiedene Größen)")

if __name__ == '__main__':
    create_icons()
