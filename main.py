import os
import asyncio
import logging
from aiohttp import web
from dotenv import load_dotenv
from pylutron_caseta.smartbridge import Smartbridge, LEAP_PORT

from bridge import Bridge
from lutron_caseta_bridge import LutronCasetaBridge

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)
# Find way to make this properly testable
bridge: Bridge = LutronCasetaBridge()

@routes.post("/scenes/{id}")
async def activate_scene_id(request):
    id = request.match_info.get('id')
    if (id in bridge.get_scenes()):
        await bridge.activate_scene(id)
        return web.Response(status=200, text=id)

    return web.Response(status=404, text=f"Scene '{id}' not found")

# Return list of available scenes
@routes.get("/scenes")
async def get_scenes(request):
    return web.json_response(data=[*bridge.get_scenes()])

# Middleware to check if the Bridge is connected before continuing
@web.middleware
async def bridge_connected_middleware(request, handler):
    if (not bridge.is_connected):
        return web.Response(status=500, text="Bridge not connected")
    return await handler(request)

# Check environment variables and connect to the bridge
async def bridge_connect():
    if (os.getenv("BRIDGE_HOST") is None):
        raise Exception("BRIDGE_HOST not set")

    try:
        logger.debug("Connecting to bridge...")
        await bridge.connect(
            host = os.getenv("BRIDGE_HOST"), 
            keyfile = os.getenv("CASETA_KEY", "caseta.key"), 
            certfile = os.getenv("CASETA_CERT", "caseta.crt"), 
            ca_cert = os.getenv("BRIDGE_CERT", "caseta-bridge.crt"),
            port = os.getenv("LEAP_PORT")
        )
        logger.debug("Connected to bridge!")
    except:
        logger.error("Failed to connect to bridge")
        return

def start_server(loop: asyncio.AbstractEventLoop):
    logger.debug("Starting server...")
    app = web.Application(middlewares=[bridge_connected_middleware])
    app.add_routes(routes)
    web.run_app(app, host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080), loop=loop)
    logger.debug("Started server!")
    
if __name__ == '__main__':
    load_dotenv(".env")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bridge_connect())
    start_server(loop)
