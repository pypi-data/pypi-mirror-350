import numpy as np
import requests

from martensite_utils import numpy_to_proto


def post_numpy_array(array: np.ndarray, url: str) -> requests.Response:
    """
    Sends the given Numpy Array to the provided URL as a serialized Protobuf Message

    :param array: The Numpy Array that will be sent as the request data.
    :param url: The URL to send the Numpy Array to
    :return: The response from the request
    """
    proto = numpy_to_proto(array)

    response = requests.post(
        url,
        data=proto.SerializeToString(),
        headers={"Content-Type": "application/octet-stream"}
    )

    return response
