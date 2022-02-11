from server import start_server
from dotenv import load_dotenv
from bridges.mock_bridge import MockBridge

if __name__ == '__main__':
    load_dotenv("example.env")
    start_server(MockBridge(), debug=True)