---
description: Technical documentation of the client.
---

# latest: version 0.3.0

### **ModelDatumType**

An enumeration of the acceptable input data types. Used to specify the type of the input and output data of a model before uploading it to the server.

| Member | Type       |
| ------ | ---------- |
| F32    | float32    |
| F64    | float64    |
| I32    | int32      |
| I64    | int64      |
| U32    | unsigned32 |
| U64    | unsigned64 |

### **connect\_server (addr, server\_name, certificate, policy, simulation, )**

Connect to the server with the specified parameters. You will have to specify here the expected policy (server identity, configuration...) and the server TLS certificate, if you are using the hardware mode.

If you're using the simulation mode, you don't need to provide a policy and certificate, but please keep in mind that this mode should NEVER be used in production as it doesn't have most of the security provided by the hardware mode.

| Param           | Type                      | description                                                                                                                     |
| --------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| addr            | `str`                     | The address of BlindAI server you want to reach.                                                                                |
| server\_name    | `str, optional`           | Contains the CN expected by the server TLS certificate. Defaults to "`blindai-srv`".                                            |
| certificate     | `Optional[str], optional` | Path to the public key of the untrusted inference server. Generated in the server side. Defaults to None.                       |
| policy          | `Optional[str], optional` | Path to the toml file describing the policy of the server. Generated in the server side. Defaults to None.                      |
| simulation      | `bool`                    | Connect to the server in simulation mode. If set to True, the args policy and certificate will be ignored. Defaults to `False`. |
| untrusted\_port | `int, optional`           | Untrusted connection server port. Defaults to `50052`.                                                                          |
| attested\_port  | `int, optional`           | Attested connection server port. Defaults to `50051`.                                                                           |

The function won't return anything if the connection was successful. In case of an issue, appropriate exceptions will be raised:

| exception type    | description                                                                                                             |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------- |
| AttestationError  | Will be raised in case the policy doesn't match the server identity and configuration, or if te attestation is invalid. |
| ConnectionError   | Will be raised if the connection with the server fails.                                                                 |
| VersionError      | Will be raised if the version of the server is not supported by the client.                                             |
| FileNotFoundError | Will be raised if the policy file, or the certificate file is not found (in Hardware mode).                             |

### **upload\_model (model, shape, dtype, dtype\_out, sign) ->** UploadModelResponse

Upload an inference model to the server.&#x20;

The provided model needs to be in the Onnx format.

| Param      | Type             | description                                                                             |
| ---------- | ---------------- | --------------------------------------------------------------------------------------- |
| model      | `str`            | Path to Onnx model file.                                                                |
| shape      | `Tuple,optional` | The shape of the model input. Defaults to None.                                         |
| dtype      | `ModelDatumType` | The type of the model input data (`f32` by default). Defaults to `ModelDatumType.F32`   |
| dtype\_out | `ModelDatumType` | The type of the model output data (`f32` by default). Defaults to `ModelDatumType.F32`. |
| sign       | `bool,optional`  | Get signed responses from the server or not. Defaults to `False`.                       |

Returns a `UploadModelResponse` object with the following fields (only if `sign` was set to `true`):

| Param       | Type                             | description                                     |
| ----------- | -------------------------------- | ----------------------------------------------- |
| payload     | `SendModelPayload`               | Raw response data                               |
| signature   | `bytes`                          | Cryptographic signature of the server response. |
| attestation | `GetSgxQuoteWithCollateralReply` | SGX attestation and collateral                  |

Content of `SendModelPayload:`

| Param       | Type    | description                        |
| ----------- | ------- | ---------------------------------- |
| model\_hash | `bytes` | SHA-256 hash of the uploaded model |
| input\_fact | `int[]` | The shape of the model input.      |

Those exceptions can be raised in case or error:

| exception type    | description                                          |
| ----------------- | ---------------------------------------------------- |
| ConnectionError   | Will be raised if the client is not connected.       |
| FileNotFoundError | Will be raised if the model file is not found.       |
| SignatureError    | Will be raised if the response signature is invalid. |

### **run\_model (data) -> RunModelResponse**

Send data to the server to make a secure inference.

The data provided must be in a list, as the tensor will be rebuilt inside the server.

| Param | Type             | description                                                                                        |
| ----- | ---------------- | -------------------------------------------------------------------------------------------------- |
| data  | `List[Any]`      | The input data. It must be an array of numbers of the same type dtype specified in `upload_model`. |
| sign  | `bool, optional` | Get signed responses from the server or not. Defaults to False.                                    |

Returns a **`RunModelResponse` ** object with the following fields:

| field  | Type        | description                                                                                  |
| ------ | ----------- | -------------------------------------------------------------------------------------------- |
| output | `List[Any]` | Output returned by the model. The format will be the same than the one set up in `dtype_out` |

The following field will be present if `sign` was set to true:

| Param       | Type                             | description                                     |
| ----------- | -------------------------------- | ----------------------------------------------- |
| payload     | `RunModelPayload`                | Raw response data                               |
| signature   | `bytes`                          | Cryptographic signature of the server response. |
| attestation | `GetSgxQuoteWithCollateralReply` | SGX attestation and collateral                  |

Content of `RunModelPayload:`

| Param         | Type             | description                                                                                  |
| ------------- | ---------------- | -------------------------------------------------------------------------------------------- |
| output        | `List[Any]`      | Output returned by the model. The format will be the same than the one set up in `dtype_out` |
| datum\_output | `ModelDatumType` | The type of the model output data.                                                           |
| input\_hash   | `bytes`          | Raw SHA-256 hash of the protobuf binary encoding of the repeatedinput from run\_model.       |

Those exceptions can be raised in case or error:

| exception type  | description                                         |
| --------------- | --------------------------------------------------- |
| ConnectionError | Will be raised if the client is not connected.      |
| SignatureError  | Will be raised if the response signature is invalid |

### UploadModelResponse/RunModelResponse.validate **(model\_hash, policy\_file, policy, validate\_quote, enclave\_signing\_key, allow\_simulation\_mode)**

Validates whether this response is valid. This is used for responses you have saved as bytes or in a file.&#x20;

This will raise an error if the response is not signed or if it is not valid.

Keep in mind that this function is automatically called, whenever sign is set to true in **`upload_model`** _and_ **`run_model.`**

| Param                   | Type                         | description                                                                              |
| ----------------------- | ---------------------------- | ---------------------------------------------------------------------------------------- |
| data\_list              | `List[Any]`                  | Input used to run the model, to validate against.                                        |
| policy\_file            | `Optional[str], optional`    | Path to the policy file. Defaults to `None`.                                             |
| policy                  | `Optional[Policy], optional` | Policy to use. Use `policy_file` to load from a file directly. Defaults to `None`.       |
| validate\_quote         | `bool, optional`             | Whether or not the attestation should be validated too. Defaults to `True`.              |
| enclave\_signing\_key   | `Optional[bytes], optional`  | Enclave signing key in case the attestation should not be validated. Defaults to `None`. |
| allow\_simulation\_mode | `bool, optional`             | Whether or not simulation mode responses should be accepted. Defaults to `False`.        |

Those exceptions can be raised in case or error:

| exception type    | description                                     |
| ----------------- | ----------------------------------------------- |
| FileNotFoundError | Will be raised if the policy file is not found. |
| SignatureError    | Signed response is invalid.                     |
| AttestationError  | Attestation is invalid.                         |

### close\_connection ( )

Close the connection between the client and the inference server.
