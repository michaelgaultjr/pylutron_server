from server import start_server
from dotenv import load_dotenv
from bridges.lutron_caseta_bridge import LutronCasetaBridge

if __name__ == '__main__':
    load_dotenv()
    start_server(LutronCasetaBridge())