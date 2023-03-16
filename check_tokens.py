from aiohttp import ClientSession
import asyncio


async def send_req(addr):
    async with ClientSession() as session:
        try:
            r = await session.get(f'https://arbitrum.foundation/_next/data/00x36Jbpql9BgTwp8Cnpi/eligibility.json?address={addr.lower()}')
            r_json = await r.json()
            if r_json == {'pageProps': {'__N_REDIRECT': '/', '__N_REDIRECT_STATUS': 307}, '__N_SSP': True}:
                print(f'[{addr}] account not exist')
            elif r_json['pageProps']['isEligible'] == True:
                print(f'[{addr}] tokens: {r_json["pageProps"]["eligibility"]["tokens"]}')
            else:
                print(f'[{addr}] tokens: 0')
        except Exception as err:
            print(f'[{addr}] error: {err}')

async def manager(addrs):
    for f in asyncio.as_completed([send_req(addr) for addr in addrs]):
        res = await f

if __name__ == '__main__':
    # print('input file with addresses: ')
    with open('addresses.txt') as f:
        addrs = f.read().splitlines()
    asyncio.run(manager(addrs))

    print('press enter to exit')
    input()