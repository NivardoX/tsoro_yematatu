import pygame
from pygame.locals import *

import client
from client import sizes
from client.chat_handler import ChatHandler

pygame.font.init()
font = pygame.font.SysFont("arial", 15)


class Chat(object):
    def __init__(self):
        self.buffer = []
        self.msg = ""

    def write(self, event):
        if event.key == K_BACKSPACE:
            self.buffer = self.buffer[0:-1]
        elif event.key == K_RETURN:
            self.buffer = []
            ChatHandler.send_message(self.msg)
        elif 32 <= event.key <= 126:
            if len(self.buffer) < 30:
                self.buffer.append(event.unicode)

        self.msg = "".join(self.buffer)

    def render(self):
        pygame.draw.rect(
            client.canvas,
            client.LIGHT_GREY,
            (sizes.MARGIN_BIG, sizes.MARGIN_BIG, sizes.CHAT_WIDTH, sizes.CHAT_HEIGHT),
        )
        pygame.draw.rect(
            client.canvas,
            (255, 255, 255),
            (
                sizes.MARGIN_BIG,
                sizes.CHAT_HEIGHT + sizes.MARGIN_BIG,
                sizes.CHAT_INPUT_BOX_WIDTH,
                sizes.CHAT_INPUT_BOX_HEIGHT,
            ),
        )
        client.canvas.blit(
            font.render(self.msg, True, (0, 0, 0)),
            (
                sizes.MARGIN_BIG + sizes.CHAT_INPUT_BOX_LEFT_MARGIN,
                sizes.CHAT_HEIGHT + sizes.MARGIN_BIG + sizes.CHAT_INPUT_BOX_TOP_MARGIN,
            ),
        )
        client.canvas.blit(
            font.render(f"{len(self.msg)}/30", True, (0, 0, 0)),
            (
                sizes.MARGIN_BIG + sizes.CHAT_INPUT_BOX_COUNTER_LEFT_MARGIN,
                sizes.MARGIN_BIG
                + sizes.CHAT_HEIGHT
                - sizes.MARGIN_TINY
                + sizes.CHAT_INPUT_BOX_COUNTER_TOP_MARGIN,
            ),
        )

        for idx, message in enumerate(ChatHandler.messages):

            pygame.draw.rect(
                client.canvas,
                (255, 255, 255),
                (
                    sizes.MARGIN_BIG,
                    sizes.MARGIN_BIG
                    + sizes.CHAT_HEIGHT
                    - sizes.CHAT_INPUT_BOX_HEIGHT
                    - (idx * sizes.CHAT_MESSAGE_MARGIN_TOP),
                    sizes.CHAT_WIDTH,
                    sizes.CHAT_MESSAGE_HEIGTH,
                ),
            )
            system_message = message.sender_type == "SYSTEM"
            client.canvas.blit(
                font.render(
                    f"Player {message.player}: {message.message}"
                    if not system_message
                    else message.message,
                    True,
                    client.RED if system_message else client.BLACK,
                ),
                (
                    sizes.MARGIN_BIG,
                    sizes.MARGIN_BIG
                    + sizes.CHAT_HEIGHT
                    - sizes.CHAT_INPUT_BOX_HEIGHT
                    - (idx * sizes.CHAT_MESSAGE_MARGIN_TOP)
                    + sizes.CHAT_MESSAGE_INNER_MARGIN_TOP,
                ),
            )
