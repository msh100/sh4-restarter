import requests
import json
from datetime import datetime, timedelta
import time
import asyncio
import logging
import os

from kasa import SmartPlug

def getSH4Stats(superhub):
    try:
        r = requests.get(f"http://{superhub}/php/ajaxGet_device_networkstatus_data.php")
        return json.loads(r.content)
    except:
        return False

def sh4Functional(superhub):
    stats = getSH4Stats(superhub)
    if not stats:
        return False

    if len(stats[3]) > 0:
        return True
    return False

def sh4Test(superhub):
    for _ in range(5):
        if sh4Functional(superhub):
            return True
        time.sleep(10)
    return False

def sleepUntilActiveHour(startHour, endHour):
    currentHour = datetime.now().hour
    if currentHour >= startHour and currentHour < endHour:
        return 0

    tomorrow = datetime.now() + timedelta(1)
    tomorrowStart = datetime(year=tomorrow.year, month=tomorrow.month,
        day=tomorrow.day, hour=startHour, minute=0, second=5)
    return (tomorrowStart - datetime.now()).seconds

async def asyncRestartSH4(smartPlug):
    plug = SmartPlug(smartPlug)

    await plug.update()
    while plug.is_on:
        await plug.turn_off()
        await plug.update()

    time.sleep(1)

    while not plug.is_on:
        await plug.turn_on()
        await plug.update()

def restartSH4(smartPlug):
    asyncio.run(asyncRestartSH4(smartPlug))

def runMainLoop(superhub, smartPlug, startHour, endHour):
    logging.debug(
        'Entered main loop '
        f'(Superhub: {superhub}, '
        f'Kasa Plug: {smartPlug}, '
        f'Run time: {startHour}-{endHour}h)',
    )
    while True:
        nextLoop = sleepUntilActiveHour(startHour, endHour)
        if nextLoop == 0:
            if not sh4Test(superhub):
                logging.info(f'Superhub 4 fails test, toggling power')
                restartSH4(smartPlug)
                logging.debug(f'Sleeping for 1 hour post Superhub 4 restart')
                time.sleep(3600)
            else:
                logging.debug('Superhub 4 is functioning correctly')
                time.sleep(60)
        else:
            logging.info(f'Sleeping until active hour ({nextLoop} seconds)')
            time.sleep(nextLoop)

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')

    if 'PLUG_IP' not in os.environ:
        raise Exception('PLUG_IP is not defined')
    smartPlug = os.environ.get('PLUG_IP')
    startHour = int(os.environ.get('START_HOUR', 2))
    endHour = int(os.environ.get('END_HOUR', 7))
    smartPlug = os.environ.get('PLUG_IP')

    runMainLoop(
        superhub="192.168.100.1",
        smartPlug=smartPlug,
        startHour=startHour,
        endHour=endHour,
    )

main()
