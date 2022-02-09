import asyncio
from dotenv import load_dotenv

from pylutron_caseta.pairing import async_pair

async def pair():
    load_dotenv()
    certs = await async_pair()

    write_cert("caseta.crt", certs["CASETA_CERT"])
    write_cert("caseta.key", certs["CASETA_KEY"])
    write_cert("caseta-bridge.crt", certs["BRIDGE_CERT"])
    print("Successfully Obtained Certificates")

def write_cert(name: str, data: str):
    file = open(name, "w")
    file.write(data)
    file.close()


# Because pylutron_caseta uses asyncio,
# it must be run within the context of an asyncio event loop.
loop = asyncio.get_event_loop()
loop.run_until_complete(pair())