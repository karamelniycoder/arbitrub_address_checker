from aiohttp import ClientSession
import asyncio


async def send_req(addr):
    async with ClientSession() as session:
        try:
            r = await session.get(f'https://arbitrum.foundation/_next/data/NDhqybgYBJYIbHFAh1PQB/eligibility.json?address={addr.lower()}')
            # print(await r.text())
            r_json = await r.json()
            if r_json == {'pageProps': {'__N_REDIRECT': '/', '__N_REDIRECT_STATUS': 307}, '__N_SSP': True}:
                print(f'[{addr}] account not exist')
            elif r_json['pageProps']['isEligible'] == True:
                tokens = r_json["pageProps"]["eligibility"]["tokens"]
                print(f'[{addr}] tokens: {tokens}')
                return int(tokens)
            else:
                print(f'[{addr}] tokens: 0')
        except Exception as err:
            print(f'[{addr}] error: {err}')

async def manager(addrs):
    total_tokens = 0
    for f in asyncio.as_completed([send_req(addr) for addr in addrs]):
        res = await f
        if type(res) == int:
            total_tokens += res
    print(f' --- Total tokens: {total_tokens} ---')

if __name__ == '__main__':
    # print('input file with addresses: ')
    with open('addresses.txt') as f:
        addrs = f.read().splitlines()
    asyncio.run(manager(addrs))

    print('press enter to exit')
    input()
