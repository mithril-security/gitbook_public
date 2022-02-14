# Hardware server

## Run the server using the docker image 🐳

### 1. Hardware requirements and drivers

You will need to have an Intel SGX ready device (with `SGX+FLC` support). Please make sure to have the `SGX+FLC` drivers (preferably with the version **1.41**) installed on your system before running the docker image. [Please check this link to have more information about the drivers.](https://github.com/intel/SGXDataCenterAttestationPrimitives/tree/master/driver/linux)

**NOTE**: There is a way to install the SGX+FLC drivers quickly without building them. All you need to do is to follow those commands:

```bash
wget https://download.01.org/intel-sgx/sgx-linux/2.15.1/distro/ubuntu18.04-server/sgx_linux_x64_driver_1.41.bin
chmod +x sgx_linux_x64_driver_1.41.bin
./sgx_linux_x64_driver_1.41.bin
```

The binary file contains the drivers signed by Intel, and will proceed to the installation transparently.

### 2. Prepare your TLS certificates

The docker image ships with a TLS certifcate by default. However, its private key is directly embedded in the public dockerhub image, therefore **it is not secure**, and should be replaced in production.

To generate a new self-signed TLS certificate, you can run

```bash
mkdir tls
openssl req -newkey rsa:2048 -nodes -keyout tls/host_server.key -out tls/host_server.pem -x509 -days 365
```

### 3. Get a PCCS API key

A [Provisioning Certificate Caching Service](https://github.com/intel/SGXDataCenterAttestationPrimitives/blob/master/QuoteGeneration/pccs/README.md) is built-in inside the Docker Image in order to generate the DCAP attestation from the enclave. You need to provide an API Key in order for the PCCS server to function. [You can get an API Key from Intel here.](https://api.portal.trustedservices.intel.com/provisioning-certification)

### 4. Run the docker image

```bash
docker run \
    -v $(pwd)/tls:/root/tls \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server:latest PCCS_API_KEY
```

## Compile the server and run it from source

In order to compile the server, you need to have the following installed on your system:

* Rust toolchain `nightly-2021-11-01`
* Cargo & Xargo
* Intel SGX SDK 2.15.100 + PSW

**You need as well to have a** [Provisioning Certificate Caching Service](https://github.com/intel/SGXDataCenterAttestationPrimitives/blob/master/QuoteGeneration/pccs/README.md) **installed on your machine in order to execute** `BlindAI` in hardware mode.

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
apt update && apt install libsgx-dcap-default-qpl-dev
git clone https://github.com/mithril-security/blindai.git
cd blindai/server
make init
make
```

Two files will be generated after the building process:

* **policy.toml :** the enclave security policy that defines which enclave is trusted.
* **host\_server.pem :** TLS certificate for the connection to the untrusted (app) part of the server.

**Those two files are needed by the client to establish a connection with the server.**

If you wish, you can also build yourself the `Docker` image with the following commands:

```bash
docker build . -f docker/hardware/hardware-ubuntu-1804.dockerfile -t blindai-server:0.1.0
```
