---
description: Technical documentation of the client.
---

# latest: version 0.2.0

### **ModelDatumType**

An enumeration of the acceptable input data types. Used to specify the type of the input data of a model before uploading it to the server.

| Member | Type       |
| ------ | ---------- |
| F32    | float32    |
| F64    | float64    |
| I32    | int32      |
| I64    | int64      |
| U32    | unsigned32 |
| U64    | unsigned64 |

### **connect\_server (addr, certificate, policy, simulation)**

Estabilish a connection with BlindAI inference server and perform the process of requesting and verifying the attestation.

| Param       | Type   | description                                                                              |
| ----------- | ------ | ---------------------------------------------------------------------------------------- |
| addr        | `str`  | the address of BlindAI server                                                            |
| certificate | `str`  | path to the public key of the untrusted inference server. Generated in the server side.  |
| policy      | `str`  | path to the toml file describing the policy of the server. Generated in the server side. |
| simulation  | `bool` | connect to the server in the simulation mode (default `False`).                          |

The function won't return anything if the connection was successful. In case of an issue, appropriate exceptions will be raised:

| exception type    | description                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------- |
| ValueError        | will be raised in case the policy doesn't match the server identity and configuration.      |
| ConnectionError   | will be raised if the connection with the server fails.                                     |
| FileNotFoundError | will be raised if the policy file, or the certificate file is not found (in Hardware mode). |

### **upload\_model (model, shape) -> SimpleReply**

Upload a pre-trained model in ONNX format to a BlindAI server.

| Param | Type             | description                      |
| ----- | ---------------- | -------------------------------- |
| model | `str`            | path to model file               |
| shape | `(int,)`         | the shape of the model input     |
| dtype | `ModelDatumType` | the type of the model input data |

Returns a **`SimpleReply`** object with the following fields:

| field | Type   | description                                |
| ----- | ------ | ------------------------------------------ |
| ok    | `bool` | True if the model is successfully uploaded |
| msg   | `str`  | message from the server                    |

Those exceptions can be raised in case or error:

| exception type    | description                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------- |
| ConnectionError   | will be raised if the connection with the server fails.                                     |
| FileNotFoundError | will be raised if the policy file, or the certificate file is not found (in Hardware mode). |

### **run\_model (data) -> ModelResult**

Send data to BlindAI server to perform the inference.

| Param | Type       | description                                                                                |
| ----- | ---------- | ------------------------------------------------------------------------------------------ |
| data  | `[number]` | array of numbers, the numbers must be of the same type `datum` specified in `upload_model` |

Returns a **`ModelResult`** object with the following fields:

| field  | Type      | description                              |
| ------ | --------- | ---------------------------------------- |
| output | `[float]` | output returned by the model             |
| ok     | `bool`    | True if the model is successfully upload |
| msg    | `str`     | message from the server                  |

Those exceptions can be raised in case or error:

| exception type      | description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| ConnectionError     | will be raised if the connection with the server fails.                                     |
| FileNotFoundError   | will be raised if the policy file, or the certificate file is not found (in Hardware mode). |
| CBOREncodeTypeError | Will be raised if the data can't be serialized.                                             |

### **close\_connection ( )**

Close the connection between the client and the inference server.
