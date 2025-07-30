import numpy as np

import martensite_utils.message_pb2 as message_pb2


numpy_types = {
    "int64": np.int64,
    "float64": np.float64,
    "float32": np.float32
}


def proto_to_numpy(proto_message: message_pb2.NDArrayProto) -> np.ndarray:
    """
    Converts a Protobuf message into a numpy array. The protobuf message must be the NDArrayProto in
    martensite_utils.message_pb2.

    :param proto_message: A martensite_utils.messasge_pb2.NDArrayProto protobuf message
    :return: The numpy array that was serialized into the protobuf message.
    """
    dtype = numpy_types[proto_message.dtype]
    array = np.frombuffer(proto_message.data, dtype=dtype).reshape(proto_message.shape)
    return array


def raw_proto_to_numpy(data: bytes) -> np.ndarray:
    """
    Converts raw bytes that were serialized using the NDArrayProto into a numpy array.

    :param data: The bytes that contain the protobuf message.
    :return: The numpy array that was serialized into the protobuf message.
    """
    proto = message_pb2.NDArrayProto()
    proto.ParseFromString(data)

    return proto_to_numpy(proto)