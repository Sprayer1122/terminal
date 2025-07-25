# VM Terminal Emulator

A responsive, full-featured terminal emulator that connects to your VM or local system via WebSocket, built with xterm.js and Python.

## Features

### Core Terminal Features
- **Full-screen black terminal** with authentic Linux terminal appearance
- **Monospaced green text** on black background for classic terminal look
- **Blinking cursor** at the command prompt
- **Keyboard input handling** with real-time command typing
- **Scrollback support** for viewing command history
- **Responsive design** that adapts to browser window size

### Interactive Shell Environment
The emulator includes a simulated Linux shell with support for common commands:

- `ls` - List directory contents (with `-l` and `-a` options)
- `pwd` - Print working directory
- `echo` - Display text
- `clear` - Clear the terminal screen
- `cd` - Change directory
- `cat` - Display file contents
- `whoami` - Show current user
- `date` - Show current date/time
- `ps` - Show running processes
- `top` - Show system resource usage
- `help` - Show available commands
- `history` - Show command history
- `exit` / `logout` - End session

### Advanced Features
- **Copy-paste support** (Ctrl+C/Ctrl+V)
- **Keyboard shortcuts**:
  - `Ctrl+C` - Cancel current command
  - `Ctrl+L` - Clear screen
  - `Ctrl+U` - Clear current line
  - `Ctrl+K` - Clear from cursor to end
  - `Up/Down arrows` - Navigate command history
- **Context menu** for copy-paste operations
- **WebGL rendering** for better performance (with fallback to canvas)
- **Responsive font sizing** for mobile devices

## Quick Start

### 1. Setup (One-time)
```bash
# Make setup script executable and run it
chmod +x setup.sh
./setup.sh
```

### 2. Start the Server
```bash
# For local access only
python3 server.py

# For remote access (from other machines)
python3 server.py --host 0.0.0.0 --port 8765
```

### 3. Connect from Browser
1. Open `terminal-emulator-ws.html` in your web browser
2. Enter your server details (host:port) in the connection modal
3. Click "Connect" to establish the connection
4. Start using real Linux commands!

## Usage

- **Local VM**: Use `localhost:8765` as connection details
- **Remote VM**: Use your VM's IP address and port (e.g., `192.168.1.100:8765`)
- **Cloud VM**: Use your cloud instance's public IP and port

## Technical Details

### Architecture
- **Frontend**: Pure HTML, CSS, and JavaScript with xterm.js
- **Backend**: Python WebSocket server with PTY support
- **Terminal Engine**: xterm.js v5.3.0
- **Addons**: FitAddon, WebLinksAddon, WebglAddon
- **Design**: Modular class-based architecture for easy extension
- **Communication**: WebSocket protocol for real-time bidirectional communication

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

### Responsive Design
- Automatically adjusts to browser window size
- Font scaling for mobile devices
- Touch-friendly interactions

## Extending the Terminal

The code is designed to be easily extensible:

### Adding New Commands
Add new command handlers in the `processCommand()` method:

```javascript
case 'newcommand':
    return this.newCommandHandler(args);
```

### VM Connection Scenarios

#### Local VM
```bash
# On your VM, start the server
python3 server.py

# In browser, connect to
localhost:8765
```

#### Remote VM (SSH)
```bash
# On remote VM, start server with external access
python3 server.py --host 0.0.0.0 --port 8765

# In browser, connect to
YOUR_VM_IP:8765
```

#### Cloud VM (AWS, GCP, Azure)
```bash
# On cloud VM, start server
python3 server.py --host 0.0.0.0 --port 8765

# Configure security group/firewall to allow port 8765
# In browser, connect to
YOUR_CLOUD_IP:8765
```

### Security Considerations
- The server runs with your user permissions
- Use firewall rules to restrict access
- Consider using HTTPS/WSS for production
- Change default port for additional security

### Custom Styling
Modify the CSS variables in the terminal theme to customize colors and appearance.

## File Structure

```
smat_ide/
├── terminal-emulator.html      # Standalone terminal emulator (simulated)
├── terminal-emulator-ws.html   # WebSocket-enabled terminal emulator
├── server.py                   # Python WebSocket server
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script
└── README.md                   # This file
```

## License

This project is open source and available under the MIT License. 