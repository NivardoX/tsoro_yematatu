import json

import grpc
import rpc.yematatu_pb2 as pb2
import rpc.yematatu_pb2_grpc as pb2_grpc


class YematatuClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self,port):

        self.host = 'localhost'
        self.server_port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.YematatuStub(self.channel)

    def send_event(self, event,data):
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

if __name__ == '__main__':
    client = YematatuClient()
    result = client.healthcheck()
    print(f'{result}')
