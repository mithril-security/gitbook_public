# BlindAI

[**Website**](https://www.mithrilsecurity.io) **|** [**LinkedIn**](https://www.linkedin.com/company/mithril-security-company) **|** [**Blog**](https://blog.mithrilsecurity.io) **|** [**Twitter**](https://www.twitter.com/mithrilsecurity) **|** [**Discord**](https://discord.gg/rWHcHeCBWk)

#### Fast, accessible and privacy friendly AI deployment 🚀🔒

**BlindAI** is a **fast, easy to use and confidential inference server**, allowing you to deploy your model on sensitive data. Thanks to the **end-to-end protection guarantees**, data owners can send private data to be analyzed by AI models, **without fearing exposing their data to anyone else**.

We reconcile _AI_ and privacy by leveraging Confidential Computing for secure inference. You can learn more about this technology here.

We currently only support _Intel SGX_, but we plan to cover _AMD SEV_ and _Nitro Enclave_ in the future. More information about our **roadmap** can be found [here](https://github.com/mithril-security/blindai/projects/1).

Our solution comes in two parts:

* A secure inference solution to serve _AI_ models with privacy guarantees.
* A _client SDK_ to securely consume the remote _AI_ models.

### Features

* Simple and fast API to use the service
* Model and data protected by hardware security
* Support of Remote Attestation with TLS (DCAP library)
* Easy to install, deploy, and maintain
* Support `SGX+FLC`

### Getting started

To deploy a model on sensitive data, with end-to-end protection, we provide a _Docker_ image to serve models with confidentiality, and a _client SDK_ to consume this service securely.

#### Note

Because the server requires specific hardware, for instance _Intel SGX_ currently, we also provide a _simulation mode_. Using the _simulation mode_, any computer can serve models with our solution. However, the two key properties of secure enclaves, data in use confidentiality, and code attestation, will not be available. **Therefore this is just for testing on your local machine but is not relevant for real guarantees in production**.

#### A - Deploying the server

Deploy the inference server, for instance using one of our _Docker_ images. To get started quickly, you can use the image with simulation, which does not require any specific hardware.

```bash
docker run -p 50051:50051 -p 50052:50052 mithrilsecuritysas/blindai-server-sim:0.1.0 
```

#### B - Sending data from the client to the server

Our _client SDK_ is rather simple, but behind the scenes, a lot happens. If we are talking to a real _enclave_ (simulation=False), the client actually verifies we are indeed talking with an _enclave_ with the right security properties, such as the code loaded inside the enclave or security patches applied. Once those checks pass, data or model can be uploaded safely, with _end-to-end protection_ through a _TLS_ tunnel ending inside the enclave. Thanks to the data in use, protection of the _enclave_ and verification of the code, everything sent remotely will not be exposed to any third party.

You can learn more about the attestation mechanism for code integrity here.

**i - Upload the model**

Then we need to load a model inside the secure inference server. First we will export our model from _Pytorch_ to _ONNX_, then we can upload it securely to the inference server. Uploading the model through our API allows the model to be kept confidential, for instance when deploying it on foreign infrastructure, like Cloud or client on-premise.

```python
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from blindai.client import BlindAiClient, ModelDatumType

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

sentence = "Hello, my dog is cute"
inputs = tokenizer(sentence, return_tensors="pt")["input_ids"]

torch.onnx.export(model,
                  inputs,
                  "./distilbert-base-uncased.onnx",
                  export_params=True,
                  opset_version=11,
                  do_constant_folding=True,
                  input_names = ['input'],
                  output_names = ['output'],
                  dynamic_axes={'input' : {0 : 'batch_size'},'output' : {0 : 'batch_size'}})

client = BlindAiClient()
client.connect_server("localhost", simulation=True)

#Upload the model to the server
response = client.upload_model(model="./distilbert-base-uncased.onnx", shape=(1, 8), datum_type=ModelDatumType.I64)
```

**ii - Send data and run model**

Upload the data securely to the inference server.

```python
from transformers import DistilBertTokenizer
from blindai.client import BlindAiClient

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

sentence = "Hello, my dog is cute"
inputs = tokenizer(sentence, padding = "max_length", max_length = 8)["input_ids"]

client = BlindAiClient()
client.connect_server("localhost", simulation=True)

#Upload the model to the server
response = client.run_model(inputs)
```

#### What you can do with BlindAI

* Easily deploy state-of-the-art models with confidentiality. Run models from **BERT** for text to **ResNets** for **images**, through **WaveNet** for audio.
* Provide guarantees to third parties, for instance clients or regulators, that you are indeed providing **data protection**, through **code attestation**.
* Explore different scenarios from confidential _Speech-to-text_, to _biometric identification_, through secure document analysis with our pool of **examples**.

#### What you cannot do with BlindAI

* Our solution aims to be modular but we have yet to incorporate tools for generic pre/post processing. Specific pipelines can be covered but will require additional handwork for now.
* We do not cover training and federated learning yet, but if this feature interests you do not hesitate to show your interest through the [roadmap](https://github.com/mithril-security/blindai/projects/1) or [Discord](https://discord.gg/rWHcHeCBWk) channel.
* The examples we provide are simple, and do not take into account complex mechanisms such as secure storage of confidential data with sealing keys, advanced scheduler for inference requests, or complex key management scenarios. If your use case involves more than what we show, do not hesitate to **contact us** for more information.

### Who made BlindAI?&#x20;

BlindAI was developed by **Mithril Security**. **Mithril Security** is a startup focused on confidential machine learning based on **Intel SGX** technology. We provide an **open source AI inference solution**, **allowing an easy and fast deployment of neural networks, with strong security properties** provided by confidential computing by performing computation in a hardware-based **Trusted Execution Environment**(_TEE_) or simply **enclaves**.

### Going further

You wish to know more about BlindAI? Great! Please have a look to the next pages to see what is under the hook.

