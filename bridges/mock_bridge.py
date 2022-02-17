import logging
from bridges.bridge import Bridge

LOG = logging.getLogger(__name__)


class MockBridge(Bridge):

    async def connect(
        self,
        host: str,
        keyfile: str,
        certfile: str,
        ca_certs: str,
        port: int = None
    ):
        LOG.debug({
            "host": host,
            "keyfile": keyfile,
            "certfile": certfile,
            "ca_certs": ca_certs,
            "port": port
        })

    @property
    def is_connected(self):
        return True

    async def activate_scene(self, scene_id: str):
        LOG.debug(f"Activated scene: '{scene_id}'")

    def get_scenes(self):
        # Mock Scenes
        return {
            "1": {
                "scene_id": "1",
                "name": "Scene 1"
            },
            "2": {
                "scene_id": "2",
                "name": "Scene 2"
            },
            "3": {
                "scene_id": "3",
                "name": "Scene 3"
            }
        }
