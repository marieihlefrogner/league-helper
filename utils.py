import json
import time
import webbrowser

champions = json.loads(open("champions.json").read())
local_settings = json.loads(open("local-settings.json").read())
debug = local_settings.get("debug", False)
open_live_game = local_settings.get("openLiveGame", False)
open_build = local_settings.get("openBuild", False)

def debug_print(*s):
    if debug:
        print(s)

def get_champion_name(id):
    return champions.get(id, None)
    
def open_u_gg_build(champ, aram=False):
    if not open_build:
        debug_print("Not opening build because it's disabled in local-settings.json")
        return
        
    if aram:
        webbrowser.open_new_tab(f"https://u.gg/lol/champions/aram/{champ}-aram")
    else:
        webbrowser.open_new_tab(f"https://u.gg/lol/champions/{champ}/build")

def open_u_gg_live_game(summoner_name):
    if not open_live_game:
        debug_print("Not opening live game stats because it's disabled in local-settings.json")
        return

    time.sleep(5)

    server = local_settings.get("server")

    if not server:
        print("ERR: local-settings.json is missing key 'server'")
        return

    debug_print("Opening live game stats for summoner", summoner_name)
    webbrowser.open(f"https://u.gg/lol/profile/{server}/{summoner_name}/live-game")

async def get(connection, method, uri):
    response = await connection.request(method, uri)
    
    if response.status > 299 or response.status < 200:
        debug_print("WARN: Failed request with status", response.status)
        return None

    json = await response.json()

    return json

async def get_current_champion(connection):
    champion = await get(connection, 'GET', '/lol-champ-select/v1/current-champion')

    try:
        champion = str(int(champion))
    except:
        return None    

    return get_champion_name(champion)

async def get_current_summoner(connection):
    response = await connection.request('get', '/lol-summoner/v1/current-summoner')

    if response.status != 200:
        debug_print("WARN: Failed to get summoner, status:", response.status)
        return None

    return await response.json()
