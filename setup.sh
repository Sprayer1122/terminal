#!/bin/bash

# Terminal Emulator Setup Script
echo "🚀 Setting up VM Terminal Emulator..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make server script executable
chmod +x server.py

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the terminal server:"
echo "   python3 server.py"
echo ""
echo "🌐 To connect from another machine:"
echo "   python3 server.py --host 0.0.0.0 --port 8765"
echo ""
echo "📱 Open terminal-emulator-ws.html in your browser to connect!"
echo ""
echo "🔧 Available options:"
echo "   --host: Server host (default: localhost)"
echo "   --port: Server port (default: 8765)"
echo "   --debug: Enable debug logging" 