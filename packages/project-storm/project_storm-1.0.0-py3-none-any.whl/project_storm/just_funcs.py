import asyncio, re
import json as json_module
from importlib.resources import files
from importlib.metadata import version as get_installed_version, PackageNotFoundError
async def c2s_search_for(ws, c2s_code: str, waiting_time: float | None = 3) -> dict | int:
    """Phrase is made from 3 letters. Returns response json or error code."""
    while True:
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=waiting_time)
            response = response.decode('utf-8')
            phrase = rf'%xt%{c2s_code}%1%(\d+)%'
            starting_info = re.search(phrase, response)
            if starting_info is not None:
                error_code = starting_info.group(1)
                if error_code == "0":
                    response = response.replace(f'%xt%{c2s_code}%1%0%', '').rstrip('%').strip()
                    return json_module.loads(response)
                else:
                    return int(error_code)
        except asyncio.TimeoutError:
            return -1

def getserver(server: str, option: str | None = "full") -> str:
    ''' Get the server URI and server prefix from the server list. 

    :option: 
    :full:  returns both websocket uri and server prefix
    :ex:  returns server prefix only
    :ws:  returns websocket uri only
    '''
    data_path = files("brunogge").joinpath("server_list.json")
    with data_path.open("r", encoding="utf-8") as f:
        data = json_module.load(f)
        wsuri = data["servers"][server]["wsuri"]
        exname = data["servers"][server]["exname"]
        if option == "full":
            return wsuri, exname
        elif option == "ex":
            return exname
        elif option == "ws":  
            return wsuri
        
async def fakescanning(ws, server: str, kid: str | None = "0") -> None:
    """
    Fake scanning the map while doing other things
    
    """
    empireex = getserver(server, "ex")
    delays = [6, 2, 4, 2]
    while ws.open:
        for delay in delays:
            print("Fake scanned...")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":0,"AY1":0,"AX2":12,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":1274,"AY1":0,"AX2":1286,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":13,"AY1":0,"AX2":25,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":1274,"AY1":13,"AX2":1286,"AY2":25}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":0,"AY1":13,"AX2":12,"AY2":25}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"{kid}":0,"AX1":13,"AY1":13,"AX2":25,"AY2":25}}%""")
            await asyncio.sleep(delay * 60) 
