# Send and Run the model

Now that the model is prepared and exported in **ONNX Format.** We will see how to use **BlindAI** to **deploy** and **run** DistilBERT. ****&#x20;

This page explains how to work with the simulation mode. This simulates Intel SGX in software, and enables you to run this on any hardware you want.

To deploy on real hardware in non-simulation mode, take a look at [deploy-on-hardware.md](../deploy-on-hardware.md "mention") and skip the first step.

To quickly setup an SGX-enabled virtual machine on Azure, take a look at [cloud-deployment](../cloud-deployment/ "mention").

## Step 1:  Run the docker image of the server

This `Docker` image provides a version of the server that allows you to test the service without having an `Intel SGX` ready device. In order to run the server in `software/simulation mode`, you can simply run this command:

```bash
docker run -it \
    -p 50051:50051 \
    -p 50052:50052 \
    mithrilsecuritysas/blindai-server-sim:latest
```

Please make sure the ports 50051 and 50052 are available

{% hint style="info" %}
Please keep in mind that this image is **not secure**, since it simulates Intel SGX in software. It is lighter than hardware mode, and should not be used in production.
{% endhint %}

### To go further...

* To build the server from the source, take a look at [hardware\_server.md](../../advanced/hardware\_server.md "mention").

## Step 2: Install the client SDK

BlindAI Client is a python package that provides a simple and straightforward way to connect with BlindAI Server.

You can install the latest version of the client using `pip`

```bash
pip install blindai 
```

{% hint style="info" %}
For now, the library is only compatible with Linux. We are working on a native Windows version, but If you are using Windows, you can still use the library with [Windows Subsystem for Linux](https://docs.microsoft.com/fr-fr/windows/wsl/install) in the meantime.&#x20;
{% endhint %}

### To go further...

* To build the Client SDK from **the source,** follow the instructions in [client\_side.md](../../advanced/client\_side.md "mention").

## &#x20;Step 3: Send the model

You can run the following script in order to send the model to the server:

```python
from blindai.client import BlindAiClient, ModelDatumType

client = BlindAiClient()

client.connect_server(addr="localhost", simulation=True)

client.upload_model(
    model="./distilbert-base-uncased.onnx", 
    shape=inputs.shape, 
    dtype=ModelDatumType.I64
    )
```

The client is straightforward, we require an address, so if you have loaded the inference server on the same machine, simply mention "localhost" as we did. For simplicity, in the simulation mode, `connect_server` simply creates an insecure channel with the server. This is meant as a quick way to test without requiring specific hardware, so **do not use the simulation mode in production**.

For the `upload_model` method, we need to specify the ONNX file, the shape of the inputs, and the type of data. Here because we run a BERT model, the inputs would be integers to represent the different tokens sent to the model.

* For more details about the client API, check the [API reference](../../resources/client-api-reference/client-interface.md).

## Step 4: Run the inference

The process is as straightforward as before, simply tokenize the input you want before sending it. As of now, the tokenization must happen at the client-side, but we will implement it shortly in the server-side, so that the client interface remains lightweight.

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

* For more details about the client API, check the [API reference](../../resources/client-api-reference/client-interface.md).

