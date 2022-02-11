import os
import asyncio
import logging
from aiohttp import web
from bridges.bridge import Bridge

__bridge: Bridge = None
routes = web.RouteTableDef()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@routes.post("/scenes/{id}")
async def activate_scene_id(request):
    id = request.match_info.get('id')
    if (id in __bridge.get_scenes()):
        await __bridge.activate_scene(id)
        return web.Response(status=200, text=id)

    return web.Response(status=404, text=f"Scene '{id}' not found")

# Return list of available scenes
@routes.get("/scenes")
async def get_scenes(request):
    return web.json_response(data=[*__bridge.get_scenes()])

# Middleware to check if the Bridge is connected before continuing
@web.middleware
async def bridge_connected_middleware(request, handler):
    if (not __bridge.is_connected):
        return web.Response(status=500, text="Bridge not connected")
    return await handler(request)

# Check environment variables and connect to the bridge
async def __bridge_connect():
    if (os.getenv("BRIDGE_HOST") is None):
        raise Exception("BRIDGE_HOST not set")

    try:
        logger.debug("Connecting to bridge...")
        await __bridge.connect(
            host=os.getenv("BRIDGE_HOST"), 
            keyfile=os.getenv("CASETA_KEY", "caseta.key"), 
            certfile=os.getenv("CASETA_CERT", "caseta.crt"), 
            ca_certs=os.getenv("BRIDGE_CERT", "caseta-bridge.crt"),
            port=os.getenv("LEAP_PORT")
        )
        logger.debug("Connected to bridge!")
    except:
        logger.error("Failed to connect to bridge")
        return

def start_server(bridge: Bridge, debug=False):
    global __bridge
    __bridge = bridge
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__bridge_connect())

    if (debug):
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug Mode Enabled")

    logger.debug("Starting server...")
    app = web.Application(middlewares=[bridge_connected_middleware])
    app.add_routes(routes)
    web.run_app(app, host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080), loop=loop)
    logger.debug("Started server!")
    
