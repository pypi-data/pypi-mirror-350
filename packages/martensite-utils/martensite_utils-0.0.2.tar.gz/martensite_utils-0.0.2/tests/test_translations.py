from martensite_utils.message_pb2 import NDArrayProto
from martensite_utils.to_numpy import proto_to_numpy, raw_proto_to_numpy
from martensite_utils.from_numpy import numpy_to_proto, numpy_to_raw_proto
import numpy as np


class TestTranslations:
    """
    This class tests the various translations that can be done using the martensite_utils library
    """

    def construct_test_message(self) -> None:
        """
        This is a helper function that manually creates a Protobuf Message and a corresponding Numpy Array. The Numpy
        Array is available at self.array and the Protobuf Message is available at self.test_message. These are used by
        calling a translation on one of these variables and comparing it with the other.
        """
        self.test_message = NDArrayProto()
        self.array = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        self.test_message.shape.extend(self.array.shape)
        self.test_message.dtype = str(self.array.dtype)
        self.test_message.data = self.array.tobytes()

    def test_to_numpy(self) -> None:
        """
        Tests the martensite_utils.proto_to_numpy() function that translates a Protobuf Message to a Numpy Array.

        Fails if the returned numpy array doesn't match self.array exactly.
        """
        self.construct_test_message()
        array = proto_to_numpy(self.test_message)
        assert (self.array == array).all()

    def test_raw_to_numpy(self):
        """
        Tests the martensite_utils.raw_proto_to_numpy() function that translates a serialized Protobuf Message to a
        Numpy Array.

        Fails if the returned Numpy Array doesn't match self.array exactly.
        """
        self.construct_test_message()
        array = raw_proto_to_numpy(self.test_message.SerializeToString())
        assert (self.array == array).all()

    def test_to_proto(self):
        """
        Tests the martensite_utils.numpy_to_proto() function that translates a Numpy Array into a Protobuf Message.

        Fails if the returned Protobuf Message doesn't match self.test_message exactly.
        """
        self.construct_test_message()
        proto_message = numpy_to_proto(self.array)

        assert proto_message.shape == self.test_message.shape
        assert proto_message.dtype == self.test_message.dtype
        assert proto_message.data == self.test_message.data

    def test_to_raw_proto(self):
        """
        Tests the martensite_utils.numpy_to_raw_proto() function that translates a Numpy Array into a serialized
        Protobuf Message.

        Fails if the returned bytes don't match the serialized version of self.test_message exactly.
        """
        self.construct_test_message()
        raw_proto = numpy_to_raw_proto(self.array)

        assert raw_proto == self.test_message.SerializeToString()