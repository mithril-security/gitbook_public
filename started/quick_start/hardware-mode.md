# Hardware Mode

### Hardware

Please make sure you're running the server in hardware mode. Please have a look to the [installation page (for the hardware mode) ](../../hardware\_server.md)first.

In the hardware mode, we will require to pass to the client the two files that were generated previously by the server, the `policy.toml` and `host_server.pem`.

If you are using the pre-built Docker image, you need to pull the policy with this command:&#x20;

```bash
wget https://raw.githubusercontent.com/mithril-security/blindai/master/examples/hardware/policy.toml
```

If you wish to use the default built-in TLS certificate, you need to pull the certificate first as well (but please remember that this certificate is **not secure**, it is strongly recommanded to [generate your own certificate](../../hardware\_server.md#2.-prepare-your-tls-certificates)):

```bash
wget https://raw.githubusercontent.com/mithril-security/blindai/master/examples/hardware/host_server.pem
```

You can now run this Python script to upload the model:

```python
from blindai.client import BlindAiClient, ModelDatumType

# Launch client
client = BlindAiClient()

client.connect_server(
    addr="localhost",
    policy="policy.toml",
    certificate="host_server.pem"
)

client.upload_model(model="./distilbert-base-uncased.onnx", shape=inputs.shape, dtype=ModelDatumType.I64)
```

The difference with the simulation mode is that, now a lot things happen under the hood when we call `connect_server`:

* a classical secure TLS connexion is first established with the host, thanks to the `host_server.pem`
* an attestation, previously generated inside the enclave, is sent to the client.
* this attestation is checked against the `policy.toml` that contains security features to expect. In case of mismatch, an error is thrown.
* once the check passes, a secure TLS connexion is established with the enclave.

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
client.connect_server(
    addr="localhost",
    policy="policy.toml",
    certificate="host_server.pem"
)

# Get prediction
response = client.run_model(inputs)
```
