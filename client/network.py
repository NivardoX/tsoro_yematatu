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

    match event:
        case "_TOGGLE_TURN":
            client.toggle_turn()
        case "PIECE_CLICKED":
            client.piece_clicked(data['tile_id'])
        case "PIECE_SELECTED_FOR_MOVEMENT":
            client.piece_selected_for_movement(data['tile_id'],data['moves'])
        case "PIECE_PLACED":
            client.piece_placed()
        case "PIECE_MOVED":
            client.piece_moved()
        case "SURRENDER":
            client.surrender(data['player'])
        case "EMPTY_TILE_CLICKED":
            client.empty_tile_clicked(data['id'])
        case "TILE_FOR_MOVEMENT_SELECTED":
            client.tile_for_movement_selected(data['id'])
        case "NEW_CHAT_MESSAGE":
            client.new_chat_message(data['sender_type'],data['message'],data['player'])
        case "TURN_VOTED":
            client.turn_voted(data['vote'])
        case "TURN_ELECTED":
            client.turn_elected(data['winner'])
        case "COLOR_PICKED":
            client.color_picked(data['color'])
        case "FINISHED":
            client.finished()

        case _:
            client.send_event(event, data)
            logger.debug(f"[{event}] server: sent: " + json.dumps(data))


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
