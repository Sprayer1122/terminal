sjcvl-amittal: /home/amittal/termina_pro/terminal >python3 server.py
/home/amittal/termina_pro/terminal/server.py:20: DeprecationWarning: websockets.server.WebSocketServerProtocol is deprecated
  from websockets.server import WebSocketServerProtocol
INFO:websockets.server:server listening on 127.0.0.1:8765
INFO:__main__:Terminal server started on ws://localhost:8765
INFO:__main__:Press Ctrl+C to stop the server
INFO:websockets.server:connection rejected (426 Upgrade Required)
ERROR:websockets.server:opening handshake failed
Traceback (most recent call last):
  File "/home/amittal/.local/lib/python3.9/site-packages/websockets/asyncio/server.py", line 356, in conn_handler
    await connection.handshake(
  File "/home/amittal/.local/lib/python3.9/site-packages/websockets/asyncio/server.py", line 207, in handshake
    raise self.protocol.handshake_exc
  File "/home/amittal/.local/lib/python3.9/site-packages/websockets/server.py", line 138, in accept
    ) = self.process_request(request)
  File "/home/amittal/.local/lib/python3.9/site-packages/websockets/server.py", line 233, in process_request
    raise InvalidUpgrade(
websockets.exceptions.InvalidUpgrade: invalid Connection header: keep-alive

