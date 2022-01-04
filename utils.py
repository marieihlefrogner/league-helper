import json
import webbrowser

champions = json.loads(open("champions.json").read())

def get_champion_name(id):
    return champions.get(id, None)
    
def open_u_gg(champ):
    webbrowser.open_new_tab(f"https://u.gg/lol/champions/aram/{champ}-aram")

async def get(connection, method, uri):
    response = await connection.request(method, uri)
    
    if response.status > 299 or response.status < 200:
        print("WARN: Failed request with status", response.status)
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