import json

import grpc
from concurrent import futures
import rpc.yematatu_pb2_grpc as pb2_grpc
import rpc.yematatu_pb2 as pb2
from client.state import receive_remote_event


class YematatuService(pb2_grpc.YematatuServicer):
    def __init__(self, *args, **kwargs):
        pass

    # General
    def SendMessage(self, request, context):
        # get the string from the incoming request
        event = request.event
        data = request.data
        from client.state import receive_remote_event

        print(data)
        receive_remote_event(event=event, data=json.loads(data))
        result = {"message": data, "received": True}

        return pb2.MessageResponse(**result)

    def HealthCheck(self, request, context):
        result = {"received": True}
        return pb2.HealthCheckReponse(**result)

    def NewChatMessage(self, request, context):
        receive_remote_event(
            event="NEW_CHAT_MESSAGE",
            data={
                "sender_type": request.sender_type,
                "message": request.message,
                "player": request.player,
            },
        )
        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def Surrender(self, request, context):
        receive_remote_event(event="SURRENDER", data={"player": request.player})
        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        # Board

    def ToggleTurn(self, request, context):
        receive_remote_event(event="_TOGGLE_TURN", data={})
        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def PieceMoved(self, request, context):
        receive_remote_event(event="PIECE_MOVED", data={})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def EmptyTileClicked(self, request, context):
        receive_remote_event(event="EMPTY_TILE_CLICKED", data={"id": request.id})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def PieceClicked(self, request, context):
        receive_remote_event(event="PIECE_CLICKED", data={"tile_id": request.tile_id})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def PiecePlaced(self, request, context):
        receive_remote_event(event="PIECE_PLACED", data={})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def PieceSelectedForMovement(self, request, context):
        receive_remote_event(
            event="PIECE_SELECTED_FOR_MOVEMENT",
            data={"tile_id": request.tile_id, "moves": request.moves},
        )

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def TileForMovementSelected(self, request, context):
        receive_remote_event(
            event="TILE_FOR_MOVEMENT_SELECTED", data={"id": request.id}
        )

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    # COLOR HANDSHAKE
    def ColorPicked(self, request, context):
        receive_remote_event(event="COLOR_PICKED", data={"color": request.color})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def Finished(self, request, context):
        receive_remote_event(event="FINISHED", data={})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        # TURN HANDSHAKE

    def TurnVoted(self, request, context):
        receive_remote_event(event="TURN_VOTED", data={"vote": request.vote})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def TurnElected(self, request, context):
        receive_remote_event(event="TURN_ELECTED", data={"winner": request.winner})

        return pb2.google_dot_protobuf_dot_empty__pb2.Empty()


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_YematatuServicer_to_server(YematatuService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
    print(f"LISTENING AT {port}")


if __name__ == "__main__":
    serve()
