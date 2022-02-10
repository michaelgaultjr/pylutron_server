from abc import abstractmethod, abstractproperty
from typing import Dict, List

class Bridge:
	@abstractmethod
	async def connect(
		self,
		host: str,
		keyfile: str,
		certfile: str,
		ca_certs: str,
		port: int = None,
	) -> None:
		pass

	@abstractproperty
	def is_connected(self) -> bool:
		pass

	@abstractmethod
	async def activate_scene(self, scene_id: str) -> None:
		pass

	@abstractmethod
	def get_scenes(self) -> Dict[str, dict]:
		pass