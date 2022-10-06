import time

from utils import get_current_champion, open_u_gg


async def aram(connection):
    time.sleep(3)

    champ = await get_current_champion(connection)

    if champ:
        print("Got", champ)
        open_u_gg(champ, aram=True)

    seconds_left = 60

    while seconds_left > 0:
        time.sleep(5)
        seconds_left -= 5

        new_champ = await get_current_champion(connection)

        if new_champ and new_champ != champ:
            champ = new_champ

            print("Changed champ to", champ)
            open_u_gg(champ, aram=True)

async def classic(connection):
    champ = None

    while not champ:
        time.sleep(2)

        champ = await get_current_champion(connection)

        if champ:
            print("Locked in champion", champ)
            open_u_gg(champ)
            break

