# Installation - Server side - Hardware

### Docker image of the server 🐳
You will need to have an Intel SGX ready device (with ```SGX+FLC``` support) in order to run this ```Docker``` image.
Please make sure to have the ```SGX+FLC``` drivers installed on your system before running the ```Docker``` image. [Please check this link to have more information about the drivers.](https://github.com/intel/linux-sgx-driver#build-and-install-the-intelr-sgx-driver)
```bash
curl -L ... | sh
```

### Compile the server and run it from source

In order to compile the server, you need to have the following installed on your system:
* Rust toolchain ```nightly-2021-11-01```
* Cargo & Xargo
* Intel SGX SDK 2.15.100 + PSW

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