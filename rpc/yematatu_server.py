import json

import grpc
from concurrent import futures
import rpc.yematatu_pb2_grpc as pb2_grpc
import rpc.yematatu_pb2 as pb2


class YematatuService(pb2_grpc.YematatuServicer):

    def __init__(self, *args, **kwargs):
        pass

    def SendMessage(self, request, context):
        # get the string from the incoming request
        event = request.event
        data = request.data
        from client.state import receive_remote_event
        print(event)
        receive_remote_event(event=event, data=json.loads(data))
        result = {'message': data, 'received': True}

        return pb2.MessageResponse(**result)

    def HealthCheck(self, request, context):
        result = {'received': True}

        return pb2.HealthCheckReponse(**result)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_YematatuServicer_to_server(YematatuService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()
    print(f"LISTENING AT {port}")


if __name__ == '__main__':
    serve()
