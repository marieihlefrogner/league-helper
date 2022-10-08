from pprint import pprint

from lcu_driver import Connector
from lcu_driver.events.responses import WebsocketEventResponse

from game_modes import aram, classic
from utils import debug_print, get_current_summoner, open_u_gg_summoner


connector = Connector()

@connector.ready
async def connect(_):
    print('LCU API is ready to be used.')

@connector.close
async def disconnect(_):
    print('The client has been closed!')

@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def gameflow_phase(connection, event: WebsocketEventResponse):
    if event.data == "ChampSelect":
        debug_print(event.uri, event.data)

        response = await connection.request("get", "/lol-gameflow/v1/session")

        if response.status != 200:
            debug_print(response, response.status)
            return

        session = await response.json()

        the_map = session.get("map")
        game_mode = the_map.get("gameMode")

        if game_mode == "ARAM":
            await aram(connection)
        elif game_mode == "CLASSIC":
            await classic(connection)
        else:
            debug_print("game mode", game_mode)

    elif event.data == "GameStart":
        summoner = await get_current_summoner(connection)

        if summoner:
            open_u_gg_summoner(summoner.get("displayName"))

    else:
        debug_print("gameflow event:", event.data)

connector.start()
