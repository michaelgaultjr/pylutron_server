import os
import asyncio
import logging
from aiohttp import web
from dotenv import load_dotenv
from pylutron_caseta.smartbridge import Smartbridge, LEAP_PORT

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)
bridge: Smartbridge = None

@routes.post("/scenes/{id}")
async def activate_scene_id(request):
    id = request.match_info.get('id')
    if (id in bridge.get_scenes()):
        await bridge.activate_scene(id)
        logger.info("Activated scene: " + id)
        return web.Response(status=200)

    return web.Response(status=404, text=f"Scene '{id}' not found")

# Return list of available scenes
@routes.get("/scenes")
async def get_scenes(request):
    return web.json_response(data=[*bridge.get_scenes()])

# Middleware to check if the Bridge is connected before continuing
@web.middleware
async def bridge_connected_middleware(request, handler):
    if (bridge is None or not bridge.logged_in):
        logger.error("Bridge not connected")
        return web.Response(status=500, text="Bridge not connected")
    return await handler(request)

# Check environment variables and connect to the bridge
async def bridge_connect():
    if (os.getenv("BRIDGE_HOST") is None):
        raise Exception("BRIDGE_HOST not set")

    global bridge
    try:
        logger.info("Connecting to bridge...")
        bridge = Smartbridge.create_tls(
            os.getenv("BRIDGE_HOST"), 
            os.getenv("CASETA_KEY", "caseta.key"), 
            os.getenv("CASETA_CERT", "caseta.crt"), 
            os.getenv("BRIDGE_CERT", "caseta-bridge.crt"),
            PORT = os.getenv("LEAP_PORT", LEAP_PORT)
        )
        await bridge.connect()
        logger.info("Connected to bridge!")
    except:
        logger.error("Failed to connect to bridge")
        return

def main():
    load_dotenv()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bridge_connect())

    # Start http server
    logger.info("Starting server...")
    app = web.Application(middlewares=[bridge_connected_middleware])
    app.add_routes(routes)
    web.run_app(app, host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8080), loop=loop)
    logger.info("Started server!")

if __name__ == '__main__':
    main()
