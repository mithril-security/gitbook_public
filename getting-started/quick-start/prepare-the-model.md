# Prepare the model

Let's assume we want to deploy a **DistilBERT** model for classification, within our confidential inference server. This could be useful for instance to analyze medical records in a privacy-friendly manner and compliant way.

Because our inference server loads ONNX models, we have to first export a **DistilBERT** in ONNX format. Pytorch or Tensorflow models can be easily exported to ONNX.

## Step 1: Load the BERT model

```python
from transformers import DistilBertForSequenceClassification

# Load the model
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
```

For simplicity, we will take a pre-trained DistilBERT without finetuning it, as the purpose is to show how to deploy a model with confidentiality.

## Step 2: Export it in ONNX format

Because it uses tracing behind the scenes, we need to feed it an example input.

```python
from transformers import DistilBertTokenizer
import torch

# Create dummy input for export
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
sentence = "I love AI and privacy!"
inputs = tokenizer(sentence, padding = "max_length", max_length = 8, return_tensors="pt")["input_ids"]

# Export the model
torch.onnx.export(
	model, inputs, "./distilbert-base-uncased.onnx",
	export_params=True, opset_version=11,
	input_names = ['input'], output_names = ['output'],
	dynamic_axes={'input' : {0 : 'batch_size'},
	'output' : {0 : 'batch_size'}})
```

