import asyncio
import json
import requests
import signal
from examine_interfaces import get_interfaces


IP_CHECK_INTERVAL = 20
REGISTRATION_INTERVAL = 10 * 60
ERROR_INTERVAL = 30
IP_SHERLOCK_DOMAIN = 'https://ip.semiversus.com'


def send_data(ip_info):
    response = requests.post(f'{IP_SHERLOCK_DOMAIN}/api/register', data=json.dumps(ip_info))
    response.raise_for_status()


async def send_data_loop_coro():
    while True:
        try:
            send_data(get_interfaces())
            print('data sent')
            await asyncio.sleep(REGISTRATION_INTERVAL)
        except requests.exceptions.HTTPError as e:
            print(f'HTTPError occured while registering: {repr(e)}')
            await asyncio.sleep(ERROR_INTERVAL)
        except requests.exceptions.ConnectionError as e:
            print(f'ConnectionError occured while registering: {repr(e)}')
            await asyncio.sleep(ERROR_INTERVAL)


async def ip_info_update_coro():
    ip_info = None
    while True:
        ip_info_new = get_interfaces()

        if ip_info != ip_info_new:

            try:
                send_data(ip_info_new)
                print('update ip_info')
                ip_info = ip_info_new
            except Exception as e:
                print(f'Exception while updating ip_info {repr(e)}')

        print('main')
        await asyncio.sleep(IP_CHECK_INTERVAL)


async def main():
    await asyncio.gather(send_data_loop_coro(), ip_info_update_coro())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, loop.stop)

    try:
        loop.run_until_complete(main())
    except Exception as e:
        print('Exception during run', repr(e))
    finally:
        print('finished')
