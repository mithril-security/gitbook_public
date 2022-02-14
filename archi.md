# Architecture

The project has several parts:

* **SCHEDULER**: Contains the main part of the program. This part is divided in three parts:
  * **TRUSTED**: `Enclave` part. Contains the `GRPC` servers (unattested server and attested server), and `Tract`, the inference library.
  * **COMMON**: Contains structure definitions and network-related functions that are common to trusted and untrusted part.
  * **UNTRUSTED**: `Host` part. Start the trusted part and contain the `RPC` `DCAP` attestation server.
* **ATTESTATION**: Contains the `DCAP attestation` library. Imported from the project Teaclave and modified for our needs.
* **API**: Contains the `proto` definition files for the unattested and attested `GRPC` servers.
* **CLIENT**: Allows the connection to the `SCHEDULER`. Contains simple functions to perform the connection and server verification according to a policy provided by the user.
