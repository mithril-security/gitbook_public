# Simulation server

### Docker image of the server 🐳

This `Docker` image provides a version of the server that allows you to test the service without having an `Intel SGX` ready device. In order to run the server in `software/simulation mode`, you can simply run this command:

```bash
sudo docker run -p 50051:50051 -p 50052:50052 mithrilsecuritysas/blindai-server-sim:latest
```

### Compile the server and run it from source

In order to compile the server, you need to have the following installed on your system:

* Rust toolchain `nightly-2021-11-01`
* Cargo & Xargo
* Intel SGX SDK 2.15.100 + PSW

You can get a Docker image having the Intel SGX SDK pre-installed [here](https://github.com/apache/incubator-teaclave-sgx-sdk#pulling-a-pre-built-docker-container). You will still need to install Xargo with the following command:

```bash
cargo install xargo
```

Once your development environment is set up, you can compile the project with those commands:

```bash
apt update && apt install libsgx-dcap-default-qpl-dev
git clone https://github.com/mithril-security/blindai.git
cd blindai/server
make init
make SGX_MODE=SW
```

If you wish, you can also build yourself the `Docker` image with the following commands:

```bash
docker build . -f docker/software/software-ubuntu-1804.dockerfile -t blindai-server-sim:latest
```
