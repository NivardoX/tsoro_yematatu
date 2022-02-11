import pygame

from client import GREY, BLACK, WHITE, state, sizes
import client
from client.point import Point


class Piece:
    def __init__(self, player, starting_point):
        self.circle = None
        self.player = player
        self.current_point = starting_point

    def propagate_click(self, pos):
        if self.circle and client.state.client_player == self.player:
            clicked = self.circle.collidepoint(pos)
            return clicked
        return False

    def render(self, x_offset=0, y_offset=0):
        self.circle = pygame.draw.circle(
            client.canvas,
            client.state.picked_colors[self.player - 1],
            (x_offset, y_offset),
            sizes.PIECE_RADIUS,
        )

        pygame.draw.circle(
            client.canvas, GREY, (x_offset, y_offset), sizes.PIECE_RADIUS, width=2
        )
