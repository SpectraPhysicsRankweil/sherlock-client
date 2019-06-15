import os
import asyncio
import json
import requests
import random
import signal
from examine_interfaces import get_interfaces


IP_CHECK_INTERVAL = 15
REGISTRATION_INTERVAL = 10 * 60
ERROR_INTERVAL = 30
IP_SHERLOCK_DOMAIN = 'ip.semiversus.com'
IDENTIFIER_PATH = '.identifier'

ip_info = {'identifier': '%016X'%random.randint(0, 0xFFFFFFFFFFFFFFFF)}


def send_data(ip_info):

    response = requests.post('https://%s/api/register'%IP_SHERLOCK_DOMAIN, data=json.dumps(ip_info))
    response.raise_for_status()


async def send_data_loop_coro():
    while True:
        try:
            ip_info.update(get_interfaces(IP_SHERLOCK_DOMAIN))
            send_data(ip_info)
            print('data sent')
            await asyncio.sleep(REGISTRATION_INTERVAL)
        except requests.exceptions.HTTPError as e:
            print('HTTPError occured while registering: %s'%repr(e))
            await asyncio.sleep(ERROR_INTERVAL)
        except requests.exceptions.ConnectionError as e:
            print('ConnectionError occured while registering: %s'%repr(e))
            await asyncio.sleep(ERROR_INTERVAL)


async def ip_info_update_coro():
    ip_info_old = None
    while True:
        ip_info.update(get_interfaces(IP_SHERLOCK_DOMAIN))

        if ip_info != ip_info_old:

            try:
                send_data(ip_info)
                print('update ip_info')
                ip_info_old = {**ip_info}
            except Exception as e:
                print('Exception while updating ip_info %s'%repr(e))

        print('try update')
        await asyncio.sleep(IP_CHECK_INTERVAL)


async def main():
    await asyncio.gather(send_data_loop_coro(), ip_info_update_coro())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, loop.stop)

    if not os.path.exists(IDENTIFIER_PATH):
        with open(IDENTIFIER_PATH, 'w') as identifier_file:
            identifier_file.write(ip_info['identifier'])
    else:
        with open(IDENTIFIER_PATH, 'r') as identifier_file:
            ip_info['identifier'] = identifier_file.read()

    print('identifier: %s'%ip_info["identifier"])

    try:
        loop.run_until_complete(main())
    except Exception as e:
        print('Exception during run', repr(e))
    finally:
        print('finished')
