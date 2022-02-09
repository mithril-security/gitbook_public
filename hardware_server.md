# Installation - Server side - Hardware

### Docker image of the server 🐳
You will need to have an Intel SGX ready device (with ```SGX+FLC``` support) in order to run this ```Docker``` image.
Please make sure to have the ```SGX+FLC``` drivers (preferably with the version 1.41) installed on your system before running the ```Docker``` image. [Please check this link to have more information about the drivers.](https://github.com/intel/SGXDataCenterAttestationPrimitives/tree/master/driver/linux)
```bash
docker run -p 50051:50051 -p 50052:50052 --device /dev/sgx/enclave --device /dev/sgx/provision blindai-server:0.1.0 API_KEY
```

A [Provisioning Certificate Caching Service](https://github.com/intel/SGXDataCenterAttestationPrimitives/blob/master/QuoteGeneration/pccs/README.md) is built-in inside the Docker Image in order to generate the DCAP attestation from the enclave. You need to provide an API Key in order for the PCCS server to function. [You can get an API Key here.](https://api.portal.trustedservices.intel.com/provisioning-certification)

### Compile the server and run it from source

In order to compile the server, you need to have the following installed on your system:
* Rust toolchain ```nightly-2021-11-01```
* Cargo & Xargo
* Intel SGX SDK 2.15.100 + PSW

**You need as well to have a** [Provisioning Certificate Caching Service](https://github.com/intel/SGXDataCenterAttestationPrimitives/blob/master/QuoteGeneration/pccs/README.md) **installed on your machine in order to execute** ```BlindAI``` in hardware mode.

You can get a Docker image having the Intel SGX SDK pre-installed [here](https://github.com/apache/incubator-teaclave-sgx-sdk#pulling-a-pre-built-docker-container). You will still need to install Xargo with the following command: 
```bash
cargo install xargo
```
Once your development environment is set up, you can compile the project with those commands: 
```bash
git clone https://github.com/mithril-security/blindai.git
cd blindai/server
make init
make
```

Two files will be generated after the building process:
- **policy.toml :** the enclave security policy that defines which enclave is trusted.
- **host_server.pem :** TLS certificate for the connection to the untrusted (app) part of the server.

**Those two files are needed by the client to establish a connection with the server.**
