"""bed_apy is a python module that talkes to minecraft via websockets"""


#stable
import asyncio
import websockets
import json
import uuid
from urllib.parse import urlparse
import base64
# Global state
send_queue = None         # Queue for outgoing commands
awaited_queue = None      # Tracks awaiting responses
websocket = None          # Active WebSocket connection
queue_tasks = None        # Background tasks (read, write, ping)
server_task = None        # WebSocket server task
max_awaited = 100         # Maximum commands awaiting a response
connection_count = 0  # Track connection messages for black magic


async def mineproxy(ws, path=None):
    """Handles incoming WebSocket connections from Minecraft."""
    global websocket, connection_count
    websocket = ws  # Store WebSocket
    connection_count+=1
    print("Minecraft connected!")
    try:
        async for raw_message in ws:
            message = json.loads(raw_message)
            if(False):
                print(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Disconnected from Minecraft.")


async def start_mc_api(host='localhost', port=3000):
    """Starts the WebSocket server."""
    async with websockets.serve(mineproxy, host=host, port=port):
        print(f"MC API running. In Minecraft, type '/connect {host}:{port}' to connect.")
        await asyncio.Future()  # Keeps the server running


async def _read_loop(debug):
    """Listens for incoming WebSocket messages."""
    global websocket
    try:
        async for raw_msg in websocket:
            msg = json.loads(raw_msg)
            if(debug):
                print("Received:", msg)
    except websockets.ConnectionClosed as e:
        print(f"WebSocket disconnected: {e}")


async def _write_loop(debug):
    """Processes and sends commands to Minecraft in controlled batches."""
    global send_queue, awaited_queue, websocket, max_awaited

    print("Write loop started—executing in batches.")
    while True:
        try:
            if not send_queue.empty():
                batch_size = min(max_awaited, send_queue.qsize())  # Max batch is 100
                command_batch = [await send_queue.get() for _ in range(batch_size)]
                
                for command_msg in command_batch:
                    print(f"Sending command: {command_msg}")
                    await websocket.send(json.dumps(command_msg))
                    awaited_queue[command_msg["header"]["requestId"]] = command_msg
                
                send_queue.task_done()
            
            await asyncio.sleep(0.5)  # Batch delay for stability

        except Exception as exc:
            print("Error in _write_loop:", exc)
            break

async def _ping_loop(debug):
    """Keeps the WebSocket connection alive with periodic pings."""
    global websocket
    while True:
        try:
            await asyncio.sleep(10)
            if(debug):
                print("Sending ping time: ")
            pong_waiter = await websocket.ping()
            await asyncio.wait_for(pong_waiter, timeout=5)
            if(debug):
                print(f"Ping acknowledged")
        except asyncio.TimeoutError:
            print("Ping failed. No pong received.")
            break
        except Exception as exc:
            print("Error in _ping_loop:", exc)
            break
async def angry_message():
    await asyncio.sleep(120) 
    decoded_message = base64.b64decode("SG93IHdlcmUgeW91IHVuYWJsZSB0byBoaXQgY3RybCtjIGN0cmwrdiBpbiAyIG1pbnV0ZXM/IERpZCB5b3Ugc3RhcnQgd2F0Y2hpbmcgdGljayB0b2Nrcz8gV2hhdCBoYXBwZW5lZCB0aGF0IHlvdSB3ZXJlIG5vdCBhYmxlIHRvIGNvcHktcGFzdGUu").decode()
    print(decoded_message)

 
async def connect(websocket_url, wdebug=False, rdebug=False, pdebug=False):
    """
    Establishes a WebSocket connection to Minecraft.

    Parameters:
      websocket_url: The URL to which you connect.
      wdebug: If True, the write loop will output debug statements.
      rdebug: If True, the read loop will output debug statements.
      pdebug: If True, the ping loop will output debug statements.
    """
    global websocket, send_queue, awaited_queue, queue_tasks, server_task, connection_count

    print(f"/connect {websocket_url}")
    parsed = urlparse(websocket_url)
    host = parsed.hostname
    port = parsed.port

    if server_task is None:
        server_task = asyncio.create_task(start_mc_api(host, port))
        print("Waiting for Minecraft to start...")

    send_queue = asyncio.Queue()
    awaited_queue = {}
    while True:  # Try until successful connection
        try:
            websocket = await websockets.connect(websocket_url)
            print("Connected successfully!")
            break
        except Exception as e:
            print(f"Connection failed: {e} — Retrying in 5 seconds...")
            await asyncio.sleep(5)
    logdata=asyncio.create_task(angry_message())
    print("Waiting for Minecraft to send an initial message...")
    while connection_count < 2:
        await asyncio.sleep(1)  # ⏳ Check every second
    print("DEBUG: Second Minecraft connection detected! Moving forward.")
    logdata.cancel
    # Start background tasks
    read_task = asyncio.create_task(_read_loop(rdebug))
    write_task = asyncio.create_task(_write_loop(wdebug))
    ping_task = asyncio.create_task(_ping_loop(pdebug))
    queue_tasks = (read_task, write_task, ping_task)

    return websocket, server_task


async def listen(event, debug=False):
    """Subscribes to an event from Minecraft."""
    global send_queue
    msg = {
        "header": {
            "version": 1,
            "requestId": str(uuid.uuid4()),
            "messageType": "commandRequest",
            "messagePurpose": "subscribe"
        },
        "body": {
            "eventName": event
        }
    }
    await send_queue.put(msg)
    if(debug):
        print(f"Subscribed to {msg}")

async def execute_on_listener(listener, function, debug=False):
    await listen(listener)  # ✅ Subscribes to event channel

    async for msg in websockets:  
        try:
            msg = json.loads(msg)  # ✅ Parses incoming message
            await function(msg)  # ✅ Calls provided function with parsed message

            if debug:
                print(f"🔍 Debug: {msg}")  # ✅ Optional debugging output

        except json.JSONDecodeError:
            print("🚨 Failed to parse incoming message JSON.")
        
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")

async def command(cmd, debug=False):
    """Queues a command to be sent to Minecraft."""
    global send_queue
    
    msg = {
        "header": {
            "version": 1,
            "requestId": str(uuid.uuid4()),
            "messagePurpose": "commandRequest",
            "messageType": "commandRequest"
        },
        "body": {
            "version": 1,
            "commandLine": cmd,
            "origin": {"type": "player"}
        }
    }
    await send_queue.put(msg)
    if(debug):
        print(f"Queued command: {msg}")


async def close():
    """Closes the WebSocket connection and cancels background tasks."""
    global queue_tasks, websocket, server_task
    if queue_tasks:
        for task in queue_tasks:
            task.cancel()
    if websocket:
        await websocket.close()
    if server_task:
        server_task.cancel()
    print("Closed Minecraft API connection.")
