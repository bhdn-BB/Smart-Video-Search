import grpc
from backend.proto import encoding_pb2, encoding_pb2_grpc

class EncodingClient:
    def __init__(self, host="localhost", port=50051):
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = encoding_pb2_grpc.EncodingServiceStub(channel)

    def encode_text(self, query: str):
        request = encoding_pb2.QueryRequest(query=query)
        return self.stub.EncodeText(request)

    def encode_images(self, images: list[bytes]):
        request = encoding_pb2.ImagesRequest(images=images)
        return self.stub.EncodeImages(request)
