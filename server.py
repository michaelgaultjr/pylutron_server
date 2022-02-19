import os
import asyncio
import logging
import jinja2
import aiohttp_jinja2
from typing import Any, Dict
from aiohttp import web
from bridges.bridge import Bridge

__bridge: Bridge = None
routes = web.RouteTableDef()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@routes.post("/api/scenes")
async def activate_scene_id(request: web.Request) -> web.Response:
    if request.has_body:
        data = await request.json()
        if ("scene_id" in data):
            id = data['scene_id']
            if (id in __bridge.get_scenes()):
                await __bridge.activate_scene(id)
                return web.Response(status=200, text=id)
            return web.Response(status=404, text=f"Scene '{id}' not found")
        return web.Response(status=400, text=f"No 'scene_id' provided")
    return web.Response(status=400, text="No body")

# Return list of available scenes


@routes.get("/api/scenes")
async def get_scenes(request: web.Request) -> web.Response:
    return web.json_response(data=[*__bridge.get_scenes()])


@routes.get("/")
@routes.post("/")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Dict[str, Any]:
    # Checks if request is a POST request
    # if it is, read request data
    # check if 'scene_id` is a valid scene
    # activate scene and redirect to '/'
    # to prevent activating scene on page reload
    if request.has_body:
        data = await request.post()
        if (data['scene_id'] in __bridge.get_scenes()):
            await __bridge.activate_scene(data['scene_id'])
            return web.HTTPFound('/')

    return {
        'scenes': __bridge.get_scenes().values()
    }

# Middleware to check if the Bridge is connected before continuing


@web.middleware
async def bridge_connected_middleware(request: web.Request, handler) -> web.Response:
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

    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(
            os.path.join(os.getcwd(), "templates"))
    )

    app.router.add_static('/static/', path='./static/', name='static')

    app.add_routes(routes)
    web.run_app(app, host=os.getenv("HOST", "0.0.0.0"),
                port=os.getenv("PORT", 8080), loop=loop)
    logger.debug("Started server!")
