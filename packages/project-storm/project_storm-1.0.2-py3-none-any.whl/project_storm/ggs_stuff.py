import websockets, asyncio, random, re
import json as json_module
from .just_funcs import getserver
async def ggs_login(ws, nick: str, pwrd: str, server: str, token: str ,kid: int | None = 0) -> tuple:
    
    """
    Login to your account and return the coordinates of your main castle.
    """
    server = getserver(server, "ex")
    aid = random.randint(100000000000000000, 999999999999999999)
    conm = random.randint(000,999)
    rtm = random.randint(00,99)
    if ws.open:
        await ws.send(f"""<msg t='sys'><body action='verChk' r='0'><ver v='166' /></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='login' r='0'><login z='{server}'><nick><![CDATA[]]></nick><pword><![CDATA[605015%pl%0]]></pword></login></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='autoJoin' r='-1'></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='roundTrip' r='1'></body></msg>""")
        await ws.send(f"""%xt%{server}%vln%1%{{"NOM": "{nick}"}}%""")
        await asyncio.sleep(0.2)
        await ws.send(f"""%xt%{server}%lli%1%{{"CONM":{conm},"RTM":{rtm},"ID":0,"PL":1,"NOM":"{nick}","PW":"{pwrd}","LT":null,"LANG":"pl","DID":"0","AID":"{aid}","KID":"","REF":"https://empire.goodgamestudios.com","GCI":"","SID":9,"PLFID":1,"RCT":"{token}"}}%""")
        await ws.send(f"%xt%{server}%nch%1%")
        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5.5)
                response = response.decode('utf-8')

                if "%xt%lli%1%" in response:
                    if "%xt%lli%1%0%" not in response:
                        print("Wrong login data.")
                        exit()
                elif "%xt%gbd%1%0%" in response:
                    response = response.replace('%xt%gbd%1%0%', '').rstrip('%').strip()
                    response = json_module.loads(response)
                    lids = []
                    fragments = response["gli"]["C"]
                    for fragment in fragments:
                        lids.append(fragment["ID"])
                    lids = sorted(lids)
                    print("Lids: ", lids)
                    break
            except asyncio.TimeoutError:
                break

        await ws.send(f"""%xt%{server}%core_gic%1%{{"T":"link","CC":"PL","RR":"html5"}}%""")
        await ws.send(f"%xt%{server}%gbl%1%{{}}%")
        await ws.send(f"""%xt%{server}%jca%1%{{"CID":-1,"KID":0}}%""")
        await ws.send(f"%xt%{server}%alb%1%{{}}%")
        await ws.send(f"%xt%{server}%sli%1%{{}}%")
        await ws.send(f"%xt%{server}%gie%1%{{}}%")
        await ws.send(f"%xt%{server}%asc%1%{{}}%")
        await ws.send(f"%xt%{server}%sie%1%{{}}%")
        await ws.send(f"""%xt%{server}%ffi%1%{{"FIDS":[1]}}%""")
        await ws.send(f"%xt%{server}%kli%1%{{}}%")
        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=4)
                response = response.decode('utf-8')
                print(response)
                if "%xt%jaa%1%0%" in response:
                    print(response)
                    sx_list = []
                    sy_list = []
                    cid_list = []
                    for i in range(4):
                        pattern = rf"\[{i},(\d+),(\d+),(\d+),1"
                        match = re.search(pattern, response)
                        cid = match.group(1)
                        sx = match.group(2)
                        sy = match.group(3)
                        sx_list.append(sx)
                        sy_list.append(sy)
                        cid_list.append(cid)
                        print(f"Coord {i} X: {sx}, Coord Y: {sy}")
                    break

            except asyncio.TimeoutError:
                break

        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5.5)
                response = response.decode('utf-8')
                if "%xt%ffi%1%0%" in response:
                    await ws.send(f"%xt%{server}%gcs%1%{{}}%")
                    print("Successfully logged in")
                    break
            except asyncio.TimeoutError:
                break
    else:
        print("Connection closed, stopping login")
    return sx_list, sy_list, lids, cid_list

async def keeping(ws, server: str) -> None:
    """Keep the connection alive by sending periodic messages."""
    while ws.open:
        try:
            await ws.send(f"%xt%{server}%pin%1%<RoundHouseKick>%")
            print("Sending keep-alive message...")
            await asyncio.sleep(60)  # Keep-alive interval
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed, stopping keep-alive")
            break

async def ggs_account(ws, nick: str, pwrd: str, server: str) -> None:
    """Login to the account and trigger next functions."""
    print("Logging in...")
    try:
        server = getserver(server, "ex")
        keepconnect = asyncio.create_task(keeping(ws, server))
        sx, sy, lids, cid = await ggs_login(ws, nick, pwrd, server)
        print("Keeping connection alive...")
        while ws.open:
            await asyncio.sleep(100)
    except websockets.exceptions.ConnectionClosedError:
        print("Theoretically you should never see this. If you do, you may be banned, idk tho.")
    