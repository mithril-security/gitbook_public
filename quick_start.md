# Get started

## Using the client

```python
from blindai.client import BlindAiClient
from PIL import Image
import numpy as np

#Create the connection
client = BlindAiClient()

client.connect_server(
    "localhost",
    policy="policy.toml",
    certificate="host_server.pem",
    simulation=False
)

#Upload the model to the server
response = client.upload_model(model="./mobilenetv2-7.onnx", shape=(1, 3, 224, 224))

if response.ok:
    print("Model loaded")
    image = Image.open("grace_hopper.jpg").resize((224,224))

    #Preprocess the data 
    a = np.asarray(image, dtype=float)
    mean =np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    a = (a / 255.0 - mean) / std
    a = np.moveaxis(a, 2, 0)

    #Send data for inference
    result = client.send_data(a.flatten())

client.close_connection()
```

In order to connect to the BlindAI server, the client needs to acquire the following files from the server: 

- **policy.toml :** the enclave security policy that defines which enclave is trusted.

- **host_server.pem :** TLS certificate for the connection to the untrusted (app) part of the server.

**Simulation mode** enables to pypass the process of requesting and checking the attestation.

Usage examples can be found in [tutorial](./tutorial) folder.

Before you run an example, make sure to get `policy.toml` and `host_server.pem` that are generated in the server side. 


## Using the server

Once the server is up and running, you can start using [the client](https://github.com/mithril-security/mithril-inference-client/tree/build_with_cmake#usgage) to start using the server.

The server has two entrypoints :
* SendModel: accept an ```ONNX``` model file as input ```([u8])```. Will return a ```SimpleReply``` object, containing a ```bool``` indicating if the loading was a success, and a ```string``` with an error message in case of problem.
* SendData: accept an array of ```f32``` as input. Will return the classification and prediction, plus a ```SimpleReply``` object.


## An example on Resnet18 (TODO)
