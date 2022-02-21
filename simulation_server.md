# Installation - Server side - Simulation

### Docker image of the server 🐳
This ```Docker``` image provides a version of the server that allows you to test the service without having an ```Intel SGX``` ready device. 
In order to run the server in ```software/simulation mode```, you can simply run this command: 
```bash
sudo docker run -p 50051:50051 -p 50052:50052 mithrilsecuritysas/blindai-server-sim:0.1.0
```

If you wish to disable telemetry, you can add the `-e BLINDAI_DISABLE_TELEMETRY=1` parameter to the run command.

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
make SGX_MODE=SW
```

Two files will be generated after the building process:
- **policy.toml :** the enclave security policy that defines which enclave is trusted.
- **host_server.pem :** TLS certificate for the connection to the untrusted (app) part of the server.

**Those two files are needed by the client to establish a connection with the server.**

If you wish, you can also build yourself the ```Docker``` image with the following commands: 
```bash
docker build . -f docker/software/software-ubuntu-1804.dockerfile -t blindai-server-sim:0.1.0
```
