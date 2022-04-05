# create an INET, STREAMing socket
import json
import socket
import threading
from time import sleep

from client import logger
from rpc.yematatu_client import YematatuClient
from rpc.yematatu_server import serve

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = None
client = None
ports = [8123, 8124]


def start_listening_thread(port):
    t = threading.Thread(target=serve, args=(port,))
    t.start()


def publish_event(event, data):
    global client
    try:

        client.send_event(event, data)
        logger.debug(f"[{event}] server: sent: " + json.dumps(data))
    except Exception as e:
        print(str(e))


def connect():
    global client
    client = YematatuClient(8123)
    if client.healthcheck():
        start_listening_thread(8124)
        return 2
    else:
        start_listening_thread(8123)
        client = YematatuClient(8124)

        while not client.healthcheck():
            logger.info("Trying to connect")
            sleep(.2)
        return 1
