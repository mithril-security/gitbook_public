## Architecture

The project has several parts:

- **SCHEDULER**: Contains the main part of the program. This part is divided in three parts: 
    -	**TRUSTED**: ```Enclave``` part. Contains the ```GRPC``` servers (unattested server and attested server), and ```Tract```, the inference library. 
    -	**COMMON**: Contains structure definitions and network-related functions that are common to trusted and untrusted part. 
    -	**UNTRUSTED**: ```Host``` part. Start the trusted part and contain the ```RPC``` ```DCAP``` attestation server.
- **ATTESTATION**: Contains the ```DCAP attestation``` library.  Imported from the project Teaclave and modified for our needs.
- **API**: Contains the ```proto``` definition files for the unattested and attested ```GRPC``` servers.
- **CLIENT**: Allows the connection to the ```SCHEDULER```. Contains simple functions to perform the connection and server verification according to a policy provided by the user.

Here’s what happens when the client will perform a connection request: 
-	The client will attempt a connection to the server
-   If we're **not in simulation mode**:
    -   The server will send a **proof of identity / DCAP Quote**
    -   The client will check if the identity match the **provided policy**
    -   If the policy match the **proof of identity**, a **TLS certificate** with the enclave identity will be given to the client
-   If we're in **simulation mode**:
    -   The client will request a **generic TLS certificate** and will not verify the policy.
-   The client is now **ready** to send a model and data.
