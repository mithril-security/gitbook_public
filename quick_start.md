# Quick Start

## An example on Distilbert

First, we start by uploading the model

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

Then, we can send our data and get our result

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
