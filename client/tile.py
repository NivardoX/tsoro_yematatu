import pygame

from client import BLUE, RED, GREY, BLACK, WHITE, LIGHT_RED, state, sizes
import client


class Tile:
    registered_events = [
        "PIECE_SELECTED_FOR_MOVEMENT",
        "PIECE_MOVED",
        "TILE_FOR_MOVEMENT_SELECTED",
    ]

    def __init__(self, id, point, piece):
        self.selected = False
        self.id = id
        self.circle = None
        self.point = point
        self.piece = piece
        self.possible_move = False

        for event in Tile.registered_events:
            state.self_register(self, event)

    def emit(self, event, data):

        client.logger.debug(f"TILE {self.id} received {event} with {data}")
        if event == "PIECE_SELECTED_FOR_MOVEMENT":
            self.possible_move = self.id in data["moves"]
            self.selected = self.id == data["tile_id"]
        if event == "PIECE_MOVED":
            self.possible_move = False
            self.selected = False

    def propagate_click(self, pos):
        if self.circle.collidepoint(pos):

            if self.circle and not self.possible_move and self.piece is None:
                state.send_event("EMPTY_TILE_CLICKED", {"id": self.id})
                return True

            if self.circle and self.possible_move:
                state.send_event("TILE_FOR_MOVEMENT_SELECTED", {"id": self.id})
                return True

        if self.piece:
            if self.piece.propagate_click(pos):
                state.send_event("PIECE_CLICKED", {"tile_id": self.id})

    def render(self, x_offset=0, y_offset=0):
        tile_x = x_offset + self.point.x
        tile_y = y_offset + self.point.y

        outer_color = client.BLACK
        if self.possible_move:
            outer_color = client.GREEN
        elif self.selected:
            outer_color = client.WHITE

        # OUTER
        pygame.draw.circle(
            client.canvas,
            outer_color,
            (tile_x, tile_y),
            sizes.TILE_RADIUS,
        )
        # INNER
        self.circle = pygame.draw.circle(
            client.canvas,
            client.GREY,
            (tile_x, tile_y),
            sizes.TILE_RADIUS - 5,
        )

        if self.piece:
            self.piece.render(tile_x, tile_y)
