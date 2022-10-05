import time

from lcu_driver import Connector
from lcu_driver.events.responses import WebsocketEventResponse

from utils import get_current_champion, open_u_gg


connector = Connector()


@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')


@connector.close
async def disconnect(_):
    print('The client has been closed!')

@connector.ws.register('/lol-gameflow/v1/gameflow-phase', event_types=('UPDATE',))
async def gameflow_phase(connection, event: WebsocketEventResponse):
    if event.data == "ChampSelect":
        print(event.uri, event.data)

        response = await connection.request("get", "/lol-gameflow/v1/session")

        if response.status != 200:
            print(response, response.status)
            return

        session = await response.json()

        the_map = session.get("map")
        game_mode = the_map.get("gameMode")

        if game_mode == "ARAM":
            time.sleep(3)

            champ = await get_current_champion(connection)

            if champ:
                print("Got", champ)
                open_u_gg(champ)

            seconds_left = 60

            while seconds_left > 0:
                time.sleep(5)
                seconds_left -= 5

                new_champ = await get_current_champion(connection)

                if new_champ and new_champ != champ:
                    champ = new_champ

                    print("Changed champ to", champ)
                    open_u_gg(champ)


connector.start()