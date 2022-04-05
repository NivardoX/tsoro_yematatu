import time

from client import GREY, network, sizes
import client
from client.ballot_box import BallotBox
from client.board import Board
import pygame

from client.chat import Chat
from client.chat_handler import ChatHandler
from client.color_picker import ColorPicker
from client.player_handshake import PlayerColorHandshake, PlayerTurnHandshake
from client.state import commit_events


def run():
    client.state.client_player = network.connect()
    ChatHandler.start()
    chat = Chat()

    victorious_player = None

    def on_victory(player):
        print("VICTORY")
        nonlocal victorious_player
        victorious_player = player

    board = Board(on_victory)
    color_picker = ColorPicker()

    # late initialization
    ballot_box = None

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("arial", sizes.BIG_FONT_SIZE)

    clock = pygame.time.Clock()
    client.canvas = pygame.display.set_mode((sizes.SCREEN_WIDTH, sizes.SCREEN_HEIGHT))

    # TITLE OF CANVAS
    pygame.display.set_caption("Tsoro Yematatu!")

    running = True
    position = 0

    # Handshakes
    PlayerColorHandshake.start()
    PlayerTurnHandshake.start()
    state = "COLOR_HANDSHAKE"
    # client.state.picked_colors = [client.LIGHT_BLUE,client.LIGHT_RED]

    while running:
        clock.tick(10)
        client.canvas.fill(GREY)


        # Player header
        if victorious_player is not None:
            textsurface = font.render(
                f"Player {victorious_player} won!", True, (0, 0, 0)
            )
        elif state == "COLOR_HANDSHAKE":
            textsurface = font.render(
                f"Player {client.state.client_player}/ {PlayerColorHandshake.human_status}",
                True,
                (0, 0, 0),
            )
        elif state == "TURN_HANDSHAKE":
            textsurface = font.render(
                f"Player {client.state.client_player}/ {PlayerTurnHandshake.human_status}",
                True,
                (0, 0, 0),
            )
        else:
            textsurface = font.render(
                f"Player {client.state.client_player}/ "
                f'''{"It's your turn!" if client.state.turn == client.state.client_player else 'Waiting for enemy move.'}''',
                True,
                (0, 0, 0),
            )
        ## Text
        client.canvas.blit(textsurface, (0, 0))
        ## Player Color
        player_color = client.state.picked_colors[client.state.client_player - 1]
        if player_color is not None:
            pygame.draw.circle(client.canvas, player_color, (40, 60), 30)

        # Handshakes
        if state == "COLOR_HANDSHAKE":
            color_picker.render(
                sizes.MARGIN_BIG * 2 + sizes.CHAT_WIDTH, sizes.MARGIN_BIG
            )

            if PlayerColorHandshake.is_finished():
                ballot_box = BallotBox()
                state = "TURN_HANDSHAKE"
                ChatHandler.send_message("TURN ELECTION STARTING", as_system=True)

        elif state == "TURN_HANDSHAKE":
            ballot_box.render(sizes.MARGIN_BIG * 2 + sizes.CHAT_WIDTH, sizes.MARGIN_BIG)
            if PlayerTurnHandshake.is_finished():
                state = "HANDSHAKES_FINISHED"
                ChatHandler.send_message("GAME STARTING", as_system=True)

        elif state == "HANDSHAKES_FINISHED":
            # Game
            board.render(sizes.MARGIN_BIG * 2 + sizes.CHAT_WIDTH, sizes.MARGIN_BIG)

        chat.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "HANDSHAKES_FINISHED":
                    board.propagate_click(pygame.mouse.get_pos())
                elif state == "COLOR_HANDSHAKE":
                    color_picker.propagate_click(pygame.mouse.get_pos())
                elif state == "TURN_HANDSHAKE":
                    ballot_box.propagate_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                chat.write(event)
        commit_events()
        pygame.display.update()

    pygame.display.quit()
