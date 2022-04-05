import random
from collections import defaultdict
from threading import Lock

import client
from client.chat_handler import ChatHandler

registered_objects = defaultdict(list)

turn_mutex = Lock()
turn = 1

availible_colors = [
    client.LIGHT_BLUE,
    client.LIGHT_RED,
    client.BLACK,
    client.WHITE,
    client.RED,
    client.BLUE,
    client.TOMATO,
    client.ORANGE,
    client.OLIVE,
    client.TEAL,
    client.INDIGO,
    client.DEEP_PINK,
]

# P1, P2
picked_colors = [None, None]
votes = [None, None]

buffered_events = []
client_player = None


def pick_color(color, player):
    ChatHandler.send_message(f"P{player} PICKED HIS COLOR", as_system=True)
    if color in availible_colors:
        picked_colors[player - 1] = color


def pick_vote(vote, player):
    ChatHandler.send_message(f"P{player} VOTED FOR {vote}", as_system=True)

    votes[player - 1] = vote


def decide_winner():
    if votes[0] == votes[1]:
        ChatHandler.send_message(f"P{votes[0]} HAS WON.", as_system=True)
        return votes[0]

    else:
        ChatHandler.send_message(
            f"THE ELECTION TIED.", as_system=True, force_publish=True
        )
        random_choice = votes[random.getrandbits(1)]
        ChatHandler.send_message(
            f"P{random_choice} WAS PICKED RANDOMLY.",
            as_system=True,
            force_publish=True,
        )
        return random_choice


def commit_event(event, data):
    for registered_object in registered_objects[event]:
        registered_object.emit(event, data)


def commit_events():
    global buffered_events
    for buffered_event in buffered_events:
        for registered_object in registered_objects[buffered_event[0]]:
            registered_object.emit(buffered_event[0], buffered_event[1])
    buffered_events = []


def receive_remote_event(event, data):
    global buffered_events

    if event == "_TOGGLE_TURN":
        buffered_events = []
        toggle_turn(publish=False)
        return
    else:
        data["_origin"] = "remote"
        commit_event(event, data)


def toggle_turn(publish=True):
    from client.network import publish_event

    global turn
    turn_mutex.acquire()
    turn = 1 if turn == 2 else 2
    if publish:
        publish_event("_TOGGLE_TURN", {})
    turn_mutex.release()


def set_turn(desired_turn, publish=True):
    global turn
    turn_mutex.acquire()
    should_toggle = not desired_turn == turn
    turn_mutex.release()

    if should_toggle:
        toggle_turn(publish)


def send_event(event, data, publish=True, emit=True, bypass_turn=False):
    from client.network import publish_event

    if bypass_turn or client.state.turn == client.state.client_player:
        if publish:
            publish_event(event, data)
        if emit:
            data["_origin"] = "local"
            buffered_events.append((event, data))


def self_register(obj, event):
    registered_objects[event].append(obj)


def reset():
    global buffered_events
    global registered_objects

    buffered_events = []
    registered_objects = defaultdict(list)
