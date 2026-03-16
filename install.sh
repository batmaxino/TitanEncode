#!/bin/bash
# ─────────────────────────────────────────────────────────────
# TitanEncode — script di installazione per CachyOS / Arch Linux
# Uso: bash install.sh
# ─────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$HOME/TitanEncode"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "╔══════════════════════════════════════════════════╗"
echo "║        TitanEncode — Installazione               ║"
echo "║        HDR Video Mastering Suite                 ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# 1. Controlla dipendenze
echo "→ Controllo dipendenze..."
MISSING=()
command -v python3 >/dev/null 2>&1 || MISSING+=("python3")
command -v ffmpeg  >/dev/null 2>&1 || MISSING+=("ffmpeg")
command -v ffprobe >/dev/null 2>&1 || MISSING+=("ffprobe (incluso in ffmpeg)")
python3 -c "import PyQt6" 2>/dev/null || MISSING+=("python-pyqt6")

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Dipendenze mancanti:"
    for dep in "${MISSING[@]}"; do
        echo "   • $dep"
    done
    echo ""
    echo "Installa con:"
    echo "   sudo pacman -S ffmpeg python-pyqt6"
    echo ""
    read -p "Vuoi continuare comunque? [s/N] " risposta
    [[ "$risposta" =~ ^[sS]$ ]] || exit 1
fi

# 2. Crea cartella applicazione
echo "→ Copio i file in $APP_DIR ..."
mkdir -p "$APP_DIR"
cp "$SCRIPT_DIR/TitanEncode.py" "$APP_DIR/TitanEncode.py" 2>/dev/null || true
chmod +x "$APP_DIR/TitanEncode.py"

# 3. Installa icona SVG
echo "→ Installo icona..."
mkdir -p "$ICON_DIR"
cp "$SCRIPT_DIR/titanencode.svg" "$HOME/.local/share/icons/hicolor/scalable/apps/titanencode.svg" 2>/dev/null || true
mkdir -p "$HOME/.local/share/icons/hicolor/scalable/apps"
cp "$SCRIPT_DIR/titanencode.svg" "$HOME/.local/share/icons/hicolor/scalable/apps/titanencode.svg"

# Converti SVG in PNG 256x256 se rsvg-convert è disponibile
if command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert -w 256 -h 256 "$SCRIPT_DIR/titanencode.svg" -o "$ICON_DIR/titanencode.png"
    echo "   ✅ Icona PNG 256x256 generata"
elif command -v convert >/dev/null 2>&1; then
    convert -background none -resize 256x256 "$SCRIPT_DIR/titanencode.svg" "$ICON_DIR/titanencode.png"
    echo "   ✅ Icona PNG 256x256 generata con ImageMagick"
else
    echo "   ℹ️  Solo SVG installato (installa librsvg o imagemagick per PNG)"
fi

# 4. Crea file .desktop con path corretto
echo "→ Creo voce nel menu applicazioni..."
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_DIR/titanencode.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=TitanEncode
GenericName=HDR Video Encoder
Comment=HDR Video Mastering Suite — x265 · x264 · VAAPI · NVENC
Exec=python3 $APP_DIR/TitanEncode.py
Icon=titanencode
Terminal=false
Categories=AudioVideo;Video;AudioVideoEditing;
Keywords=video;encode;hdr;hevc;x265;mkv;film;mastering;
StartupNotify=true
StartupWMClass=TitanEncode
EOF
chmod +x "$DESKTOP_DIR/titanencode.desktop"

# 5. Aggiorna database icone e menu
echo "→ Aggiorno database icone e menu..."
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
kbuildsycoca6 2>/dev/null || kbuildsycoca5 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✅  TitanEncode installato correttamente!       ║"
echo "║                                                  ║"
echo "║  Trovi TitanEncode in:                           ║"
echo "║  Menu KDE → Multimedia → TitanEncode             ║"
echo "║                                                  ║"
echo "║  Oppure avvia con:                               ║"
echo "║  python3 ~/TitanEncode/TitanEncode.py            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "ℹ️  Se l'icona non appare subito, esci e rientra in KDE"
echo "   oppure esegui: kbuildsycoca6"
