# Get started

## Using the server

Once the server is up and running, you can start using [the client](https://github.com/mithril-security/mithril-inference-client/tree/build_with_cmake#usgage) to start using the server.

The server has two entrypoints :
* SendModel: accept an ```ONNX``` model file as input ```([u8])```. Will return a ```SimpleReply``` object, containing a ```bool``` indicating if the loading was a success, and a ```string``` with an error message in case of problem.
* SendData: accept an array of ```f32``` as input. Will return the classification and prediction, plus a ```SimpleReply``` object.

## Using the client (TODO)

## An example on Resnet18 (TODO)
