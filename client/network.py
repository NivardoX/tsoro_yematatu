# create an INET, STREAMing socket
import json
import socket
import threading

from client import logger

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = None


def handle_client(conn, addr):
    from client.state import receive_remote_event

    while True:
        message = conn.recv(1024)
        message = message.decode()
        packets = message.split("\n")
        for packet in packets:
            if packet != "":
                logger.debug("[thread] client: recv: " + str(packet))
                receive_remote_event(**json.loads(packet))


def start_listining_thread(c, addr):
    t = threading.Thread(target=handle_client, args=(c, addr))
    t.start()


def publish_event(event, data):
    socket = c or s
    packet = json.dumps({"event": event, "data": data})
    socket.send((packet + "\n").encode())
    logger.debug("[thread] server: sent: " + packet)


def connect():
    try:
        logger.info("Trying to connect")
        s.connect(("127.0.0.1", 8123))
        start_listining_thread(s, "localhost")
        logger.info("Connected")

        return 2
    except Exception:
        logger.info("Not able to connect. Becoming the server.")
        global c
        # No one listening, become the server
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8123))
        s.listen(20)
        logger.info("Waiting for connection")
        c, addr = s.accept()
        start_listining_thread(c, addr)
        return 1
