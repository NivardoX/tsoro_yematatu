import dataclasses
from typing import Optional

from client import state, sizes


class ChatHandler:
    messages = []

    @classmethod
    def start(cls):
        state.self_register(cls, "NEW_CHAT_MESSAGE")

    @classmethod
    def add_message_to_buffer(cls, message):
        if len(cls.messages) == sizes.CHAT_NUMBER_OF_MESSAGES:
            cls.messages.pop(-1)
        cls.messages.insert(0, message)

    @classmethod
    def emit(cls, event, data):
        message = Message(
            data["sender_type"],
            data["message"],
            data["player"],
        )
        cls.add_message_to_buffer(message)

    @classmethod
    def send_message(cls, msg, as_system=False, force_publish=False):
        if as_system:
            message = Message("SYSTEM", message=msg, player=None)
            cls.add_message_to_buffer(message)
            if force_publish:
                state.send_event(
                    "NEW_CHAT_MESSAGE",
                    dataclasses.asdict(message),
                    emit=False,
                    bypass_turn=True,
                )
        else:
            message = Message("PLAYER", message=msg, player=state.client_player)
            cls.add_message_to_buffer(message)
            state.send_event(
                "NEW_CHAT_MESSAGE",
                dataclasses.asdict(message),
                emit=False,
                bypass_turn=True,
            )


@dataclasses.dataclass
class Message:
    sender_type: str
    message: str
    player: Optional[int]
