import aiohttp
import re
from aiohttp import web

import models
from pikabot_graphs import settings
from restycorn.restycorn.server import Server
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource

import asyncio
import logging
import asyncpgsa

from server.communities import communities, get_community_graph_item_resource
from server.index import index, user_distributions
from server.pikabu_new_year_18_game import top_items, scoreboards
from server.users import pikabu_users, users, get_user_graph_item_resource


async def pre_request(request: aiohttp.ClientRequest):
    if 'PHPSESS' in request.cookies:
        session = request.cookies['PHPSESS']
        if session in settings.ALLOWED_USERS_SESSIONS:
            return None

    return web.Response(text="""
<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Google?</title>
    <style>
    html, body {
        height: 100%;
        padding: 0;
        margin: 0;
    }
    body {
        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: stretch;
        align-content: center;
    }
    h1 {
        text-align: center;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        align-content: center;
        font-size: 30px;
        color: #aeaeae;
    }
    h1 img {
        height: 50px;
        margin-left: 10px;
    }
    input[type="text"] {
        /* border: 1px solid: #eee; */
        border: none;
        padding: 10px 20px;
        margin: 0;
        background-color: #fff;
        height: 44px;
        vertical-align: top;
        border-radius: 2px;
        transition: box-shadow 200ms cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 2px 2px 0 rgba(0,0,0,0.16),0 0 0 1px rgba(0,0,0,0.08);
        font-size: 18px;
    }
    input[type="text"]:hover,
    input[type="text"]:valid {
        box-shadow: 0 3px 8px 0 rgba(0,0,0,0.2),0 0 0 1px rgba(0,0,0,0.08);
    }
    #google {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        align-content: center;
    }
    #google form {
        width: 50%;
    }
    #google form > * {
        display: block;
        width: 100%;
        margin-bottom: 25px;
    }
    #google form > div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        align-content: center;
    }
    #google form > div > * {
        margin: 0 5px;
        height: 36px;
        line-height: 27px;
        background-image: -moz-linear-gradient(top,#f5f5f5,#f1f1f1);
        -moz-border-radius: 2px;
        -moz-user-select: none;
        background-color: #f2f2f2;
        border: 1px solid #f2f2f2;
        border-radius: 2px;
        color: #757575;
        cursor: default;
        font-family: arial,sans-serif;
        font-size: 13px;
        font-weight: bold;
        margin: 11px 4px;
        min-width: 54px;
        padding: 0 16px;
        text-align: center;
    }
    #google form > div > *:hover {
        border: 1px solid #aeaeae;
        color: #000;
    }
    </style>
</head>

<body>
    <h1>
        This is not 
        <img src="https://www.google.com.ua/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png">
    </h1>
    <div id="google">
        <form id="googleForm" action="https://www.google.com/search" method="GET" onsubmit="return processForm()">
            <input name="q" id="googleSearchText" type="text" required>
            <div>
                <input name="btnK" value="Not Google Search" type="submit">
                <input name="btnI" value="I'm not feeling Lucky" type="submit">
            </div>
        </form>
    </div>
    <script>
    function setCookie(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    function processForm(e) {    
        const searchText = googleSearchText.value.trim();
        if (/^[a-z0-9A-Z]{64,64}$/.test(searchText)) {
            setCookie('PHPSESS', searchText);
            location.reload();
            return false;
        }
        return true;
    }
    </script>
</body>
</html>
    """, headers={
        'Content-Type': 'text/html',
    })


async def default_route(request: aiohttp.ClientRequest):
    path = request.path

    if path == '/':
        path = '/index.html'

    if re.match(r'^(/([a-zA-Z0-9_]+(.[a-zA-Z0-9]+)*)?)+$', path):
        try:
            with open('./frontend/dist/' + path, 'r'):
                return web.FileResponse('./frontend/dist/' + path)
        except (FileNotFoundError, IsADirectoryError):
            pass

    return web.FileResponse('./frontend/dist/index.html')

    # return web.Response(text="""
    # <img src="http://richdoctor.ru/wp-content/uploads/2018/01/Prekratite-zapreshheno.jpg">
    # """, headers={'Content-Type': 'text/html'})


async def create_server():
    await asyncpgsa.pg.init(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
        min_size=5,
        max_size=100,
    )

    server = Server(
        '127.0.0.1',
        access_log_format='%Tfs %a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"')
    server.set_base_address('/api')

    server.pre_request_function = pre_request

    server.set_default_route(default_route)

    server.register_resource('index', index)
    server.register_resource('graph/distribution/user', user_distributions)
    server.register_resource('users', users)
    server.register_resource('pikabu_users', pikabu_users)
    server.register_resource('communities', communities)

    server.register_resource('graph/user/rating', get_user_graph_item_resource(models.core_userratingentry))
    server.register_resource('graph/user/subscribers',
                             get_user_graph_item_resource(models.core_usersubscriberscountentry))
    server.register_resource('graph/user/comments', get_user_graph_item_resource(models.core_usercommentscountentry))
    server.register_resource('graph/user/posts', get_user_graph_item_resource(models.core_userpostscountentry))
    server.register_resource('graph/user/hot_posts', get_user_graph_item_resource(models.core_userhotpostscountentry))
    server.register_resource('graph/user/pluses', get_user_graph_item_resource(models.core_userplusescountentry))
    server.register_resource('graph/user/minuses', get_user_graph_item_resource(models.core_userminusescountentry))

    server.register_resource('graph/community/subscribers_count',
                             get_community_graph_item_resource('subscribers_count'))
    server.register_resource('graph/community/stories_count', get_community_graph_item_resource('stories_count'))

    server.register_resource('new_year_2018_game/top_items', top_items)
    server.register_resource('new_year_2018_game/scoreboards', scoreboards)

    # logging
    logger = logging.getLogger('aiohttp.access')

    logger.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler('logs/{}.error.log'.format('aiohttp.access'))
    error_file_handler.setLevel(logging.ERROR)
    info_file_handler = logging.FileHandler('logs/{}.log'.format('aiohttp.access'))
    info_file_handler.setLevel(logging.INFO)

    logger.addHandler(error_file_handler)
    logger.addHandler(info_file_handler)

    if settings.DEBUG:
        debug_file_handler = logging.FileHandler('logs/{}.debug.log'.format('aiohttp.access'))
        debug_file_handler.setLevel(logging.DEBUG)
        logger.addHandler(debug_file_handler)

    return server


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_server()).run()
