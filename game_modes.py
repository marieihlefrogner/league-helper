import time

from utils import debug_print, get_current_champion, open_u_gg


async def aram(connection):
    time.sleep(3)

    champ = await get_current_champion(connection)

    if champ:
        debug_print("Got champion:", champ)
        open_u_gg(champ, aram=True)

    seconds_left = 60

    while seconds_left > 0:
        time.sleep(5)
        seconds_left -= 5

        new_champ = await get_current_champion(connection)

        if new_champ and new_champ != champ:
            champ = new_champ

            debug_print("Changed champion to:", champ)
            open_u_gg(champ, aram=True)

async def classic(connection):
    champ = None

    while not champ:
        time.sleep(2)

        champ = await get_current_champion(connection)

        if champ:
            debug_print("Locked in champion:", champ)
            open_u_gg(champ)
            break

