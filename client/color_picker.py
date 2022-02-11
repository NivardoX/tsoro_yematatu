import pygame
import client.state
from client import sizes
from client.player_handshake import PlayerColorHandshake


class ColorPicker:
    def __init__(self):
        self.selectors = [
            ColorSelector(i, color)
            for i, color in enumerate(client.state.availible_colors)
        ]

    def render(self, x_offset=0, y_offset=0):
        for selector in self.selectors:
            selector.render(x_offset, y_offset)

    def propagate_click(self, pos):
        if len(self.selectors):
            for selector in self.selectors:
                clicked = selector.propagate_click(pos)
                if clicked:
                    break
        return False


class ColorSelector:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.picked = False
        self.rect = None

        client.state.self_register(self, "COLOR_PICKED")

    def render(self, x_offset=0, y_offset=0):

        self.rect = pygame.Rect(
            (self.id % 4 * (sizes.COLOR_SELECOR_WIDTH + sizes.MARGIN_SMALL)) + x_offset,
            (self.id // 4 * (sizes.COLOR_SELECOR_HEIGHT + sizes.MARGIN_SMALL))
            + y_offset,
            sizes.COLOR_SELECOR_WIDTH,
            sizes.COLOR_SELECOR_HEIGHT,
        )
        pygame.draw.rect(
            client.canvas, client.LIGHT_GREY if self.picked else self.color, self.rect
        )

    def propagate_click(self, pos):
        if self.rect and not self.picked and PlayerColorHandshake.should_pick():
            clicked = self.rect.collidepoint(pos)
            if clicked:
                PlayerColorHandshake.pick(self.color)
                self.picked = True
            return clicked
        return False

    def emit(self, event, data):
        if tuple(data["color"]) == tuple(self.color):
            self.picked = True
