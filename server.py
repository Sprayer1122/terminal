#!/usr/bin/env python3
"""
WebSocket Server for Terminal Emulator
Connects browser terminal to real VM/system commands
"""

import asyncio
import json
import logging
import os
import pty
import signal
import subprocess
import sys
import termios
import tty
from typing import Optional

import websockets
from websockets.server import serve

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TerminalSession:
    """Manages a single terminal session with PTY"""
    
    def __init__(self, websocket):
        self.websocket = websocket
        self.master_fd = None
        self.slave_fd = None
        self.process = None
        self.running = False
        
    async def start(self):
        """Start the terminal session with PTY"""
        try:
            # Create PTY
            self.master_fd, self.slave_fd = pty.openpty()
            
            # Start shell process
            shell_cmd = os.environ.get('SHELL', '/bin/bash')
            self.process = subprocess.Popen(
                [shell_cmd],
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                preexec_fn=os.setsid,
                start_new_session=True
            )
            
            self.running = True
            
            # Start read/write tasks
            asyncio.create_task(self._read_from_pty())
            asyncio.create_task(self._read_from_websocket())
            
            logger.info(f"Terminal session started with PID {self.process.pid}")
            
        except Exception as e:
            logger.error(f"Failed to start terminal session: {e}")
            await self.websocket.close(1011, f"Failed to start terminal: {e}")
    
    async def _read_from_pty(self):
        """Read from PTY and send to WebSocket"""
        try:
            while self.running and self.process and self.process.poll() is None:
                try:
                    # Read from master PTY
                    data = os.read(self.master_fd, 1024)
                    if data:
                        # Send to WebSocket
                        await self.websocket.send(json.dumps({
                            'type': 'output',
                            'data': data.decode('utf-8', errors='replace')
                        }))
                    else:
                        await asyncio.sleep(0.01)
                except OSError:
                    break
        except Exception as e:
            logger.error(f"Error reading from PTY: {e}")
        finally:
            await self._cleanup()
    
    async def _read_from_websocket(self):
        """Read from WebSocket and send to PTY"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    if data['type'] == 'input':
                        # Write to master PTY
                        os.write(self.master_fd, data['data'].encode('utf-8'))
                    elif data['type'] == 'resize':
                        # Handle terminal resize
                        self._resize_terminal(data['cols'], data['rows'])
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON received")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error reading from WebSocket: {e}")
        finally:
            await self._cleanup()
    
    def _resize_terminal(self, cols: int, rows: int):
        """Resize the terminal"""
        try:
            import fcntl
            import struct
            
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, winsize)
        except Exception as e:
            logger.warning(f"Failed to resize terminal: {e}")
    
    async def _cleanup(self):
        """Clean up the terminal session"""
        self.running = False
        
        if self.process:
            try:
                # Send SIGTERM to process group
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                
                # Wait for process to terminate
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't terminate
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    self.process.wait()
            except Exception as e:
                logger.error(f"Error terminating process: {e}")
        
        # Close file descriptors
        if self.master_fd:
            os.close(self.master_fd)
        if self.slave_fd:
            os.close(self.slave_fd)
        
        # Close WebSocket
        if not self.websocket.closed:
            await self.websocket.close()

async def handle_connection(websocket, path):
    """Handle new WebSocket connection"""
    client_ip = websocket.remote_address[0] if websocket.remote_address else 'unknown'
    logger.info(f"New connection from {client_ip}")
    
    # Create terminal session
    session = TerminalSession(websocket)
    
    try:
        # Start the terminal session
        await session.start()
        
        # Keep connection alive
        await websocket.wait_closed()
        
    except Exception as e:
        logger.error(f"Error handling connection: {e}")
    finally:
        logger.info(f"Connection from {client_ip} closed")

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Terminal WebSocket Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8765, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Terminal server starting on ws://{args.host}:{args.port}")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        async with serve(handle_connection, args.host, args.port):
            await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main()) 
