# Simulation server

## Docker image of the server 🐳

This `Docker` image provides a version of the server that allows you to test the service without having an `Intel SGX` ready device. In order to run the server in `software/simulation mode`, you can simply run this command:

```bash
sudo docker run -p 50051:50051 -p 50052:50052 mithrilsecuritysas/blindai-server-sim:latest
```

Please keep in mind that this image is **not secure**, since it simulates Intel SGX in software. It is lighter than hardware mode, and should not be used in production.

## Compile the server and run it from source (using Docker 🐳)

You can build the whole project by using our Dockerimage. We did set up the Dockerimage to have a reproductible build no matter the environment. You can start the process with this command:&#x20;

```bash
cd server
make init
DOCKER_BUILDKIT=1 docker build --target software -t mithrilsecuritysas/blindai-server-sim:latest . -f ./docker/build.dockerfile
```

As you're building the project in software mode, there is no extra steps needed to run the server. You can directly use the [command above](simulation\_server.md#docker-image-of-the-server) to start the Docker image.

## Compile the server and run it from source

In order to compile the server, you need to have the following installed on your system:

* Rust toolchain `nightly-2021-11-01`
* Cargo & Xargo
* Intel SGX SDK 2.15.100 + PSW

You can get a Docker image having the Intel SGX SDK pre-installed [here](https://github.com/apache/incubator-teaclave-sgx-sdk#pulling-a-pre-built-docker-container). You will still need to install Xargo with the following command:

```bash
cargo install xargo
```

If you are building the project using the Docker Image provided above, you will need to install the SGX Default Quote Provider Library:&#x20;

```bash
apt update && apt install -y libsgx-dcap-default-qpl-dev
```

Once your development environment is set up, you can compile the project with those commands:

```bash
git clone https://github.com/mithril-security/blindai.git
cd blindai/server
make init
make SGX_MODE=SW
```
