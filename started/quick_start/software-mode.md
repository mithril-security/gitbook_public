# Software Mode

### Simulation

You can easily run BlindAI with this command:&#x20;

```bash
docker run -p 50051:50051 -p 50052:50052 mithrilsecuritysas/blindai-server-sim:latest
```

You can now run this Python script to upload the model:

```python
from blindai.client import BlindAiClient, ModelDatumType

# Launch client
client = BlindAiClient()

client.connect_server(addr="localhost", simulation=True)

client.upload_model(model="./distilbert-base-uncased.onnx", shape=inputs.shape, dtype=ModelDatumType.I64)
```

The client is straightforward, we require an address, so if you have loaded the inference server on the same machine, simply mention "localhost" as we did. For simplicity, in simulation `connect_server` simply creates an insecure channel to the server. This is meant as a quick way to test without requiring specific hardware, so **do not use the simulation mode in production**.

For the `upload_model` method, we need to specify the ONNX file, the shape of the inputs, and the type of data. Here because we run a BERT model, the inputs would be integers to represent the different tokens sent to the model.

### Step 4: Run the model

The process is as straight forward as before, simply tokenize the input you want before sending it. As of now, the tokenization must happen at the client side, but we will implement it shortly in the server side, so that client interface remains lightweight.

```python
from transformers import DistilBertTokenizer

# Prepare the inputs
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
sentence = "I love AI and privacy!"
inputs = tokenizer(sentence, padding = "max_length", max_length = 8)["input_ids"]
```

Now we simply have to create our client, connect and send data to be analyzed. In the same fashion as before, we will create a client in simulation, and simply send data to be analyzed with the proper communication channel.

```python
from blindai.client import BlindAiClient

# Load the client
client = BlindAiClient()
client.connect_server("localhost", simulation=True)

# Get prediction
response = client.run_model(inputs)
```
