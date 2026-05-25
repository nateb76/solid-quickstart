#!/bin/bash
# Build vAI Send Mail as a standalone macOS .app
# Run this from the vai-send-mail directory on your Mac.

set -e

echo ""
echo "╔══════════════════════════════════════╗"
echo "║    Building vAI Send Mail .app       ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Ensure we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: Run this script from the vai-send-mail directory."
    exit 1
fi

# Create/activate venv if needed
if [ ! -d ".venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv .venv
fi

echo "→ Activating virtual environment..."
source .venv/bin/activate

echo "→ Installing dependencies..."
pip install -r requirements.txt
pip install pywebview pyinstaller

echo "→ Building .app with PyInstaller..."
pyinstaller vai_send_mail.spec --clean --noconfirm

echo ""
echo "════════════════════════════════════════"
echo "  Build complete!"
echo ""
echo "  Your app is at:"
echo "    dist/vAI Send Mail.app"
echo ""
echo "  To install, drag it to /Applications."
echo ""
echo "  First launch: right-click → Open"
echo "  (macOS blocks unsigned apps on first run)"
echo "════════════════════════════════════════"
echo ""
