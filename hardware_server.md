# Hardware server

## Run the server using the Docker image 🐳

### 1. Hardware requirements and drivers

You will need to have an Intel SGX ready device (with `SGX+FLC` support). Please make sure to have the `SGX+FLC` drivers (preferably with the version **1.41**) installed on your system before running the docker image. [Please check this link to have more information about the drivers.](https://github.com/intel/SGXDataCenterAttestationPrimitives/tree/master/driver/linux)

**NOTE**: There is a way to install the SGX+FLC drivers quickly without building them. All you need to do is to follow those commands:

```bash
wget https://download.01.org/intel-sgx/sgx-linux/2.15.1/distro/ubuntu18.04-server/sgx_linux_x64_driver_1.41.bin
chmod +x sgx_linux_x64_driver_1.41.bin
./sgx_linux_x64_driver_1.41.bin
```

The binary file contains the drivers signed by Intel, and will proceed to the installation transparently.

### 2. Get a PCCS API key

A [Provisioning Certificate Caching Service](https://github.com/intel/SGXDataCenterAttestationPrimitives/blob/master/QuoteGeneration/pccs/README.md) is built-in inside the Docker Image in order to generate the DCAP attestation from the enclave. You need to provide an API Key in order for the PCCS server to function. [You can get an API Key from Intel here.](https://api.portal.trustedservices.intel.com/provisioning-certification)

### 3. Run the docker image

You can easily run the Docker image with this command:&#x20;

```bash
docker run \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server:latest /root/start.sh PCCS_API_KEY
```

If you wish to disable telemetry, you can add the `-e BLINDAI_DISABLE_TELEMETRY=1` parameter to the run command.

You can easily get the policy and certificate using wget, with these commands:&#x20;

```bash
wget https://raw.githubusercontent.com/mithril-security/blindai/master/examples/distilbert/hardware/policy.toml
wget https://raw.githubusercontent.com/mithril-security/blindai/master/examples/distilbert/hardware/host_server.pem
```

### Advanced - Extract policy and default TLS certificate from the Docker Image

You can extract the policy directly from the Docker Image using:

```
docker run mithrilsecuritysas/blindai-server:latest /bin/cat /root/policy.toml > policy.toml
```

You can also extract the default TLS certificate like this:&#x20;

```
docker run mithrilsecuritysas/blindai-server:latest /bin/cat /root/tls/host_server.pem > host_server.pem
```

### Advanced - Prepare your TLS certificates and inject it into BlindAI

As you readed above, the Docker image ships with a TLS certifcate by default. However, its private key is directly embedded in the public Docker hub image, therefore **it is not secure**, and should be replaced in production.

To generate a new self-signed TLS certificate, you can run

```bash
mkdir tls
openssl req -newkey rsa:2048 -nodes -keyout tls/host_server.key -out tls/host_server.pem -x509 -days 365
```

Once you generated your TLS certificate, you can use it with the project:

```bash
docker run \
    -v $(pwd)/tls:/root/tls \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server:latest /root/start.sh PCCS_API_KEY
```

`-v $(pwd)/tls:/root/tls` allows you to mount your own TLS certificate to the Docker Image.&#x20;

## Compile the server and run it from source (using Docker 🐳)

You can build the whole project by using our Dockerimage. We did set up the Dockerimage to have a reproducible build no matter the environment. You can start the process with those commands:

```bash
cd server
make init
DOCKER_BUILDKIT=1 docker build --target hardware -t mithrilsecuritysas/blindai-server:latest . -f ./docker/build.dockerfile
```

To run the client, you will want to get the `policy.toml` file from the server using:

```bash
docker run mithrilsecuritysas/blindai-server:latest /bin/cat /root/policy.toml > policy.toml
```

You will need the file `host_server.pem` as well, you will find this file in the folder `bin/tls.`

You can now start the Docker image using this command:

```bash
docker run \
    -v $(pwd)/bin/tls:/root/tls \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server:latest /root/start.sh PCCS_API_KEY
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

If you are building the project using the Docker Image provided above, you will need to install the SGX Default Quote Provider Library:

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
