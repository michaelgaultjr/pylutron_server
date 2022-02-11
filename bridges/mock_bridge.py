import logging
from bridges.bridge import Bridge

class MockBridge(Bridge):
	__logger = logging.getLogger(__name__)

	async def connect(
			self,
			host: str,
			keyfile: str,
			certfile: str,
			ca_certs: str,
			port: int = None
		):
		self.__logger.debug({
			"host": host,
			"keyfile": keyfile,
			"certfile": certfile,
			"ca_certs": ca_certs,
			"port": port
		})

	@property
	def is_connected(self):
		return True;

	async def activate_scene(self, scene_id: str):
		self.__logger.debug(f"Activated scene: '{scene_id}'")

	def get_scenes(self):
		# Mock Scenes
		return { 
			"scene1": { 
				"id":"scene1", 
				"name": "Scene 1"
			}, 
			"scene2": { 
				"id":"scene2", 
				"name": "Scene 2"
			}, 
			"scene3": { 
				"id":"scene3", 
				"name": "Scene 3" 
			} 
		}