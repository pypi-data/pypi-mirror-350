# Martensite Utils

Welcome to Martensite Utils! This Python package is developed by Stonecrest 
Data Solutions and is designed to be used in conjunction with our Martensite
Docker Container. It is a simple package that is designed to handle the
transmission of Numpy Arrays over TCP by serializing the Arrays into a Protobuf
Message. Since a lot of this is complex and usually outside the normal realm of
AI/ML Engineers, we developed Martensite Utils to simplify this process.

Though Martensite Utils was designed to be used with Martensite, we can see the
potential benefit of using it in other projects that need to send Numpy Arrays
over TCP and would encourage this type of usage.

## Usage

There are a handful of translations that are included in Martensite Utils:

* Numpy Array -> Protobuf Message (`numpy_to_proto()`)
* Numpy Array -> Serialized Protobuf Message (`numpy_to_raw_proto()`)
* Protobuf Message -> Numpy Array (`proto_to_numpy()`)
* Serialized Protobuf Message -> Numpy Array (`raw_proto_to_numpy()`)

The typical process that is used for sending a Numpy Array to an endpoint is:

1. Create Numpy Array
2. Translate Numpy Array to Protobuf Message
3. Serialize Protobuf Message
4. Attach serialized Protobuf Message to request data
5. Send request

And to receive a Numpy Array:

1. Receive Request
2. Deserialize request data as Protobuf Message
3. Translate Protobuf Message into Numpy Array

**Note**: For both sending and receiving, steps 2&3 can be replaced by their
corresponding "raw" calls.

### Example

This example code creates a random Numpy Array, translates it to a serialized
Protobuf Message, sends it to the inference endpoint of a locally hosted
Martensite server, then parses the received data into a Numpy Array.

```python
import numpy as np
import requests
from martensite_utils import numpy_to_raw_proto
from martensite_utils import raw_proto_to_numpy

input_array = np.random.random((10, 10))
input_data = numpy_to_raw_proto(input_array)

response = requests.post(
    url="http://127.0.0.1:8000/inference",
    data=input_data
)

received_data = raw_proto_to_numpy(response.content)
print(f"Result: {received_data}")
```

There is also a helper function at `martensite_utils.post_numpy_array()` that
takes care of the translation and transmission all at once. View its docstring
to learn how to use it.