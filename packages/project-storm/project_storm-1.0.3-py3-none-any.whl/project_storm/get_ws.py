import asyncio, websockets
from .just_funcs import getserver

async def ggs_ws(server: str) -> websockets.WebSocketClientProtocol:
    """
    Connect to the GGS websocket server and return the websocket object.
    """
    server = getserver(server, "ws")
    try:
        ws = await websockets.connect(server, ping_interval=None) ###GGS chce swoje
        print(f"Connected to {server}")
        return ws
    except websockets.exceptions.ClientClosedError as e:
        print(f"Unexpected error, maybe someone else logged in? {e}")
        raise e
    except Exception as e:
        print(f"Error connecting to {server}: {e}")
        return None