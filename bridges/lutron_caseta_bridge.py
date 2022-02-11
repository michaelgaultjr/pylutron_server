import logging
from bridges.bridge import Bridge
from pylutron_caseta.smartbridge import Smartbridge, LEAP_PORT

class LutronCasetaBridge(Bridge):
	__logger = logging.getLogger(__name__)
	__bridge: Smartbridge = None

	async def connect(
			self,
			host: str,
			keyfile: str,
			certfile: str,
			ca_certs: str,
			port: int = None
		):
		if (port is None): 
			port = LEAP_PORT

		self.__bridge: Smartbridge = Smartbridge.create_tls(
				hostname=host, 
				port=port,
				keyfile=keyfile,
				certfile=certfile,
				ca_certs=ca_certs,
		)
		await self.__bridge.connect()

	@property
	def is_connected(self):
		return self.__bridge is not None and self.__bridge.is_connected

	async def activate_scene(self, scene_id: str):
		await self.__bridge.activate_scene(scene_id)
		self.__logger.debug("Activated scene: " + id)

	def get_scenes(self):
		return self.__bridge.get_scenes()
