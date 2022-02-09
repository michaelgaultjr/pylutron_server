import os
import asyncio
from typing import Dict
from dotenv import load_dotenv
from aiohttp import web
from pylutron_caseta.smartbridge import Smartbridge, LEAP_PORT

bridge: Smartbridge = None

async def connect():
    bridge: Smartbridge = Smartbridge.create_tls(
        os.getenv("BRIDGE_IP"), 
        os.getenv("CASETA_KEY", "caseta.key"), 
        os.getenv("CASETA_CERT", "caseta.crt"), 
        os.getenv("BRIDGE_CERT", "caseta-bridge.crt"),
        PORT = os.getenv("LEAP_PORT", LEAP_PORT)
    )
    await bridge.connect()

    scenes = bridge.get_scenes()
    print("Scenes: " + str(scenes.keys()))

    return bridge;

async def handle_activate_scene(request):
    if (bridge is None and bridge.logged_in):
        raise web.Response(status=500, text="Bridge not connected")
    id = request.match_info.get('id')
    if (id in bridge.get_scenes()):
        await bridge.activate_scene(id)
        return web.Response(status=200)
    return web.Response(status=404,text="Scene not found")

app = web.Application()
app.add_routes([web.get('/scene/{id}', handle_activate_scene)])

async def main():
    load_dotenv()
    if (os.getenv("BRIDGE_IP") is None):
        raise Exception("BRIDGE_IP not set")

    global bridge
    bridge = await connect();

    web.run_app(app)

if __name__ == '__main__':
    # Not sure which of these works
    # asyncio.run(main());
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())