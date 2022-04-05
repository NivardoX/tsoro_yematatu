import json

import grpc
import rpc.yematatu_pb2 as pb2
import rpc.yematatu_pb2_grpc as pb2_grpc


class YematatuClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self, port):

        self.host = 'localhost'
        self.server_port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.YematatuStub(self.channel)

    def send_event(self, event, data):
        """
        Client function to call the rpc for GetServerResponse
        """

        message = pb2.Message(event=event, data=json.dumps(data))
        return self.stub.SendMessage(message)

    def healthcheck(self):
        """
        Client function to call the rpc for GetServerResponse
        """

        try:
            return self.stub.HealthCheck(pb2.google_dot_protobuf_dot_empty__pb2.Empty()).received
        except Exception:
            return False

    def toggle_turn(self):
        return self.stub.ToggleTurn(pb2.google_dot_protobuf_dot_empty__pb2.Empty())

    def piece_clicked(self, tile_id):
        return self.stub.PieceClicked(pb2.PieceClickedMessage(tile_id=tile_id))

    def piece_selected_for_movement(self, tile_id, moves):
        return self.stub.PieceSelectedForMovement(pb2.PieceSelectedForMovementMessage(tile_id=tile_id, moves=moves))

    def piece_moved(self):
        return self.stub.PieceMoved(pb2.google_dot_protobuf_dot_empty__pb2.Empty())

    def piece_placed(self):
        return self.stub.PiecePlaced(pb2.google_dot_protobuf_dot_empty__pb2.Empty())

    def surrender(self, player):
        return self.stub.Surrender(pb2.SurrenderMessage(player=player))

    def empty_tile_clicked(self, id):
        return self.stub.EmptyTileClicked(pb2.EmptyTileClickedMessage(id=id))

    def tile_for_movement_selected(self, id):
        return self.stub.TileForMovementSelected(pb2.TileForMovementSelectedMessage(id=id))

    def new_chat_message(self, sender_type, message, player):
        return self.stub.NewChatMessage(pb2.ChatMessage(sender_type=sender_type, message=message, player=player))

    def turn_voted(self, vote):
        return self.stub.TurnVoted(pb2.TurnVotedMessage(vote=vote))

    def turn_elected(self, winner):
        return self.stub.TurnElected(pb2.TurnElectedMessage(winner=winner))

    def color_picked(self, color):
        return self.stub.ColorPicked(pb2.ColorPickedMessage(color=color))

    def finished(self):
        return self.stub.Finished(pb2.google_dot_protobuf_dot_empty__pb2.Empty())


if __name__ == '__main__':
    client = YematatuClient()
    result = client.healthcheck()
    print(f'{result}')
