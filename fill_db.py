import asyncio
import traceback

import aiohttp
import sys

from add_user import add_user_by_username


async def main():
    async with aiohttp.ClientSession() as session:
        for page in range(1, int(sys.argv[1]) + 1):
            async with session.get('https://pikagraphs.d3d.info/api/pikabu_users/?page={}'.format(page)) as response:
                json_response = await response.json()
                print(json_response.keys())
                for user in json_response['results']:
                    print(user['username'])
                    try:
                        add_user_by_username(user['username'])
                    except BaseException as ex:
                        print(type(ex))
                        print(ex)
                        traceback.print_exc()



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
