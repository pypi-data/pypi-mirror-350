import numpy as np

import martensite_utils.message_pb2 as message_pb2


def numpy_to_proto(array: np.ndarray) -> message_pb2.NDArrayProto:
    """
    Converts a Numpy Array into a Protobuf message. The Protobuf message will
    be an NDArrayProto message.

    :param array: The Numpy Array object to translate into the Protobuf message.
    :return: The Protobuf message.
    """

    proto_message = message_pb2.NDArrayProto()

    proto_message.shape.extend(array.shape)
    proto_message.data = array.tobytes()
    proto_message.dtype = str(array.dtype)
    return proto_message


def numpy_to_raw_proto(array: np.ndarray) -> bytes:
    """
    Converts a Numpy Array into a serialized Protobuf message, ready to be sent
    to a server as bytes.

    :param array:  
    :return:
    """
    proto = numpy_to_proto(array)
    return proto.SerializeToString()