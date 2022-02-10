import os
import asyncio
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

from pylutron_caseta.pairing import async_pair

async def pair():
    load_dotenv()
    logger.info("Starting pairing...")
    certs = await async_pair()

    logger.info("Pairing successful, writing certificiates...")
    write_cert(os.getenv("CASETA_KEY", "caseta.key"), certs["PAIR_KEY"])
    write_cert(os.getenv("CASETA_CERT", "caseta.crt"), certs["PAIR_CERT"])
    write_cert(os.getenv("BRIDGE_CERT", "caseta-bridge.crt"), certs["PAIR_CA"])
    logger.info("Wrote certificates, pairing complete!")

def write_cert(name: str, data: str):
    file = open(name, "w")
    file.write(data)
    file.close()


# Because pylutron_caseta uses asyncio,
# it must be run within the context of an asyncio event loop.
loop = asyncio.get_event_loop()
loop.run_until_complete(pair())