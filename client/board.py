import pygame

import client
from client import state, sizes
from client.chat_handler import ChatHandler
from client.piece import Piece
from client.state import send_event, toggle_turn
from client.tile import Tile
from client.point import Point

pygame.font.init()
font = pygame.font.SysFont("arial", sizes.MEDIUM_FONT_SIZE)
font2 = pygame.font.SysFont("arial", sizes.SMALL_FONT_SIZE)


class Board:
    def __init__(self, on_victory):
        self.on_vitory = on_victory
        self.width = sizes.BOARD_WIDTH
        self.height = sizes.BOARD_HEIGHT
        self.unit = sizes.MARGIN_BIG
        self.tiles = [
            Tile(0, Point(self.width // 2, self.unit), None),
            Tile(1, Point(self.width - self.unit * 5, self.height // 2), None),
            Tile(2, Point(self.width // 2, self.height // 2), None),
            Tile(3, Point(self.unit * 2 + self.unit * 3, self.height // 2), None),
            Tile(4, Point(self.unit * 2, self.height - self.unit), None),
            Tile(5, Point(self.width // 2, self.height - self.unit), None),
            Tile(6, Point(self.width - self.unit * 2, self.height - self.unit), None),
        ]
        self.status = "WAITING_FOR_PIECE"
        self.selected_piece = None
        self.pieces_placed = 0
        self.surrender_rect = None
        state.self_register(self, "PIECE_CLICKED")
        state.self_register(self, "EMPTY_TILE_CLICKED")
        state.self_register(self, "TILE_FOR_MOVEMENT_SELECTED")
        state.self_register(self, "PIECE_PLACED")
        state.self_register(self, "PIECE_MOVED")
        state.self_register(self, "SURRENDER")

    def emit(self, event, data):
        player = client.state.turn
        if event == "SURRENDER":
            surrendered_player = 1 if data['player'] == 2 else 1
            self.on_vitory(surrendered_player)
            ChatHandler.send_message(f"PLAYER {data['player']} SURRENDERED",as_system=True)
        if event == "TILE_FOR_MOVEMENT_SELECTED":
            if self.status == "WAITING_FOR_PIECE_FOR_MOVEMENT":
                moved_piece = self.selected_piece

                self.tiles[moved_piece.current_point].piece = None

                moved_piece.current_point = data["id"]
                self.tiles[data["id"]].piece = moved_piece
                self.selected_piece = None
                self.status = "WAITING_FOR_PIECE_FOR_MOVEMENT"
                send_event("PIECE_MOVED", {})

        elif event == "PIECE_CLICKED":
            if self.status == "WAITING_FOR_PIECE_FOR_MOVEMENT":
                piece = self.tiles[data["tile_id"]].piece
                moves = self.calculate_possible_moves(piece)
                if not len(moves):
                    return
                self.selected_piece = piece
                self.status = "WAITING_FOR_PIECE_FOR_MOVEMENT"
                send_event(
                    "PIECE_SELECTED_FOR_MOVEMENT",
                    {"tile_id": data["tile_id"], "moves": moves},
                )

        elif event == "EMPTY_TILE_CLICKED":
            if self.status == "WAITING_FOR_PIECE":
                self.tiles[data["id"]].piece = Piece(player, data["id"])
                self.pieces_placed += 1
                if self.pieces_placed == 6:
                    self.status = "WAITING_FOR_PIECE_FOR_MOVEMENT"
                send_event("PIECE_PLACED", {})

        elif event == "PIECE_PLACED" or event == "PIECE_MOVED":
            self.check_vitory()
            if client.state.turn == client.state.client_player:
                toggle_turn()

    def calculate_possible_moves(self, piece):
        moves = []

        tile_id = piece.current_point
        neightboors = {
            0: [1, 2, 3, 4, 5, 6],
            1: [0, 2, 3, 4],
            2: [0, 1, 3, 5],
            3: [0, 1, 2, 6],
            4: [0, 1, 5, 6],
            5: [0, 2, 4, 6],
            6: [0, 3, 4, 5],
        }
        for neightboor in neightboors[tile_id]:
            if not self.tiles[neightboor].piece:
                moves.append(neightboor)
        return moves

    def check_vitory(self):
        lines = [
            [0, 1, 4],
            [0, 2, 5],
            [0, 3, 6],
            [1, 2, 3],
            [4, 5, 6],
        ]

        for line in lines:
            players = [
                self.tiles[id].piece.player for id in line if self.tiles[id].piece
            ]

            if players.count(2) == 3:
                self.on_vitory(2)
                self.status = "VICTORY"
            if players.count(1) == 3:
                self.on_vitory(1)
                self.status = "VICTORY"

    def propagate_click(self, pos):
        if self.surrender_rect.collidepoint(pos):
            send_event("SURRENDER",{"player":client.state.client_player},bypass_turn=True)
            return True
        if client.state.turn == client.state.client_player:
            for tile in self.tiles:
                if tile.propagate_click(pos):
                    break

    def render(self, x_offset=0, y_offset=0):
        pygame.draw.rect(
            client.canvas,
            client.LIGHT_GREY,
            pygame.Rect(
                x_offset,
                y_offset,
                self.width,
                self.height,
            ),
        )

        def get_tile_position(index):
            return tuple(
                (
                    x_offset + self.tiles[index].point.x,
                    y_offset + self.tiles[index].point.y,
                )
            )

        pygame.draw.line(
            client.canvas,
            client.BLACK,
            get_tile_position(0),
            get_tile_position(5),
            width=2,
        )
        pygame.draw.line(
            client.canvas,
            client.BLACK,
            get_tile_position(0),
            get_tile_position(4),
            width=2,
        )
        pygame.draw.line(
            client.canvas,
            client.BLACK,
            get_tile_position(0),
            get_tile_position(6),
            width=2,
        )
        pygame.draw.line(
            client.canvas,
            client.BLACK,
            get_tile_position(1),
            get_tile_position(3),
            width=2,
        )
        pygame.draw.line(
            client.canvas,
            client.BLACK,
            get_tile_position(4),
            get_tile_position(6),
            width=2,
        )

        self.surrender_rect = pygame.Rect(
            sizes.SCREEN_WIDTH - sizes.MARGIN_SMALL - sizes.SURRENDER_BUTTON_WIDTH,
            sizes.MARGIN_SMALL,
            sizes.SURRENDER_BUTTON_WIDTH,
            sizes.SURRENDER_BUTTON_HEIGHT,
        )
        pygame.draw.rect(
            client.canvas,
            client.BLACK,
            pygame.Rect(
                sizes.SCREEN_WIDTH - sizes.MARGIN_SMALL - sizes.SURRENDER_BUTTON_WIDTH,
                sizes.MARGIN_SMALL,
                sizes.SURRENDER_BUTTON_WIDTH,
                sizes.SURRENDER_BUTTON_HEIGHT,
            ),
            width=2
        )
        pygame.draw.rect(
            client.canvas,
            client.DARK_GREY,
            self.surrender_rect,
        )

        client.canvas.blit(
            font.render("SURRENDER", True, (0, 0, 0)),
            (
                sizes.SCREEN_WIDTH - sizes.SURRENDER_BUTTON_WIDTH+ 2*sizes.MARGIN_SMALL,
                2*sizes.MARGIN_TINY+sizes.SURRENDER_BUTTON_HEIGHT//2,
            ),
        )

        for tile in self.tiles:
            tile.render(x_offset, y_offset)
