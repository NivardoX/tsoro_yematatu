import abc
from client import state, logger


# Sync Handshake
class PlayerColorHandshake:
    status = None
    stauts_messages_map = {
        "COLOR_PICKED": "Waiting for other player.",
        "PICKING_COLOR": "It's your turn to pick a color.",
        "WAITING_FOR_OTHER_PLAYER": "Waiting for other player to pick his color.",
        "FINISHED": "Starting election.",
    }

    @classmethod
    @property
    def human_status(cls):
        return cls.stauts_messages_map.get(cls.status, "")

    @classmethod
    def is_finished(cls):
        return cls.status == "FINISHED"

    @classmethod
    def start(cls):
        events = ["COLOR_PICKED", "FINISHED"]
        for event in events:
            state.self_register(cls, event)
        cls.status = (
            "WAITING_FOR_OTHER_PLAYER" if state.client_player == 2 else "PICKING_COLOR"
        )

    @classmethod
    def should_pick(cls):
        return cls.status == "PICKING_COLOR"

    @classmethod
    def pick(cls, color):
        state.pick_color(color, state.client_player)
        cls.status = "COLOR_PICKED"
        cls.communicate("COLOR_PICKED", {"color": color})
        state.toggle_turn()

    @classmethod
    def communicate(cls, status, data):
        logger.debug(f"PlayerColorHandshake sending {status} with {cls.status}")
        state.send_event(status, data, emit=False)

    @classmethod
    def emit(cls, other_status, data):
        logger.debug(f"PlayerColorHandshake receiving {other_status} with {cls.status}")
        if other_status == "COLOR_PICKED":
            state.pick_color(tuple(data["color"]), 1 if state.client_player == 2 else 2)
            if cls.status == "WAITING_FOR_OTHER_PLAYER":
                cls.status = "PICKING_COLOR"
            elif cls.status == "COLOR_PICKED":
                cls.status = "FINISHED"
                state.toggle_turn()
                cls.communicate("FINISHED", {})

        if other_status == "FINISHED":
            cls.status = "FINISHED"
            state.toggle_turn()


# Sync Handshake
class PlayerTurnHandshake:
    status = None
    stauts_messages_map = {
        "WAITING_FOR_OTHER_PLAYER_TO_VOTE": "Waiting for other player.",
        "TURN_VOTED": "Waiting for other player.",
        "VOTING_FOR_TURN": "It's your turn to vote. Who should start?",
        "FINISHED_TURN_VOTING": "Starting the game.",
    }

    @classmethod
    @property
    def human_status(cls):
        return cls.stauts_messages_map.get(cls.status, "")

    @classmethod
    def is_finished(cls):
        return cls.status == "FINISHED_TURN_VOTING"

    @classmethod
    def start(cls):
        events = ["TURN_VOTED", "TURN_ELECTED"]
        for event in events:
            state.self_register(cls, event)
        cls.status = (
            "WAITING_FOR_OTHER_PLAYER_TO_VOTE"
            if state.client_player == 2
            else "VOTING_FOR_TURN"
        )

    @classmethod
    def should_vote(cls):
        return cls.status == "VOTING_FOR_TURN"

    @classmethod
    def vote(cls, vote):
        state.pick_vote(vote, state.client_player)
        cls.status = "TURN_VOTED"
        cls.communicate("TURN_VOTED", {"vote": vote})
        state.toggle_turn()

    @classmethod
    def communicate(cls, status, data):
        logger.debug(f"PlayerTurnHandshake sending {status} with {cls.status}")
        state.send_event(status, data, emit=False)

    @classmethod
    def emit(cls, other_status, data):
        logger.debug(f"PlayerTurnHandshake receiving {other_status} with {cls.status}")
        if other_status == "TURN_VOTED":
            state.pick_vote(data["vote"], 1 if state.client_player == 2 else 2)
            if cls.status == "WAITING_FOR_OTHER_PLAYER_TO_VOTE":
                cls.status = "VOTING_FOR_TURN"
            elif cls.status == "TURN_VOTED":
                cls.status = "FINISHED_TURN_VOTING"
                state.toggle_turn()
                cls.communicate("TURN_ELECTED", {"winner": state.decide_winner()})

        if other_status == "TURN_ELECTED":
            cls.status = "FINISHED_TURN_VOTING"
            state.set_turn(data["winner"])
