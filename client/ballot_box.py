import pygame

import client.state
from client import sizes
from client.player_handshake import PlayerColorHandshake, PlayerTurnHandshake


class BallotBox:
    def __init__(self):
        self.ballots = [
            Ballot(1, client.state.picked_colors[0], self.on_vote),
            Ballot(2, client.state.picked_colors[1], self.on_vote),
        ]

    def on_vote(self):
        if len(self.ballots):
            for ballot in self.ballots:
                ballot.color = client.LIGHT_GREY

    def render(self, x_offset=0, y_offset=0):
        for selector in self.ballots:
            selector.render(x_offset, y_offset)

    def propagate_click(self, pos):
        if len(self.ballots):
            for ballot in self.ballots:
                clicked = ballot.propagate_click(pos)
                if clicked:
                    break
        return False


class Ballot:
    def __init__(self, id, color, on_vote):
        self.id = id
        self.color = color
        self.on_vote = on_vote
        self.rect = None

    def render(self, x_offset=0, y_offset=0):
        self.rect = pygame.Rect(
            ((self.id - 1) * (sizes.BALLOT_WIDTH + sizes.MARGIN_SMALL)) + x_offset,
            sizes.MARGIN_SMALL + y_offset,
            sizes.BALLOT_WIDTH,
            sizes.BALLOT_HEIGHT,
        )
        pygame.draw.rect(client.canvas, self.color, self.rect)

    def propagate_click(self, pos):
        if self.rect and PlayerTurnHandshake.should_vote():
            clicked = self.rect.collidepoint(pos)
            if clicked:
                PlayerTurnHandshake.vote(self.id)
                self.on_vote()
            return clicked
        return False
