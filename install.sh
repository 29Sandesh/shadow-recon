#!/usr/bin/env bash
# SHADOW-RECON v1.0 - 1-Line Global Installer (Linux / macOS)

set -e

echo "================================================================================"
echo "   🌐  SHADOW-RECON v1.0: B2B COMPANY & DOMAIN OSINT INTELLIGENCE SCANNER"
echo "================================================================================"

INSTALL_DIR="$HOME/.shadow-recon"
mkdir -p "$INSTALL_DIR"

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required. Please install python3 and pip3."
    exit 1
fi

echo "[1/3] Installing Python dependencies..."
pip3 install requests dnspython beautifulsoup4 --quiet

echo "[2/3] Downloading latest Shadow-Recon release..."
if [ -d "./shadow_recon" ]; then
    cp -r ./* "$INSTALL_DIR/"
else
    curl -sL https://github.com/29Sandesh/shadow-recon/archive/refs/heads/main.tar.gz | tar -xz -C "$INSTALL_DIR" --strip-components=1
fi

echo "[3/3] Linking 'shadow-recon' and 'recon' to /usr/local/bin..."
WRAPPER="$INSTALL_DIR/shadow-recon"
cat << 'EOF' > "$WRAPPER"
#!/usr/bin/env bash
PYTHONPATH="$HOME/.shadow-recon" python3 -m shadow_recon.cli "$@"
EOF
chmod +x "$WRAPPER"

if [ -w "/usr/local/bin" ]; then
    ln -sf "$WRAPPER" /usr/local/bin/shadow-recon
    ln -sf "$WRAPPER" /usr/local/bin/recon
else
    echo "export PATH="$INSTALL_DIR:\$PATH"" >> "$HOME/.bashrc"
fi

echo ""
echo "================================================================================"
echo "  ✅ INSTALLATION COMPLETE! Run 'shadow-recon <domain>' or 'recon <domain>'"
echo "================================================================================"
