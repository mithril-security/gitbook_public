# Hardware server - Azure DCs v3

## Run the server using the Docker image 🐳

The VMs Azure DCs v3 offers great performance right out of the box, thanks to the new version of Intel SGX and the support of a new processor architecture named Ice Lake SP.&#x20;

However, because of the way those VMs were setup, we cannot use the classical hardware version of BlindAI, we need to use a special patched version of the project, supporting the attestation and verification system provided by Microsoft.&#x20;

### 1. Run the docker image

You can easily run the Docker image with this command:&#x20;

```bash
docker run \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server-dcsv3:latest
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
docker run mithrilsecuritysas/blindai-server-dcsv3:latest /bin/cat /root/policy.toml > policy.toml
```

You can also extract the default TLS certificate like this:&#x20;

```
docker run mithrilsecuritysas/blindai-server-dcsv3:latest /bin/cat /root/tls/host_server.pem > host_server.pem
```

### Advanced - Prepare your TLS certificates and inject it into BlindAI

As you read above, the Docker image ships with a TLS certifcate by default. However, its private key is directly embedded in the public Docker hub image, therefore **it is not secure**, and should be replaced in production.

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
    mithrilsecuritysas/blindai-server-dcsv3:latest
```

`-v $(pwd)/tls:/root/tls` allows you to mount your own TLS certificate to the Docker Image.&#x20;

## Compile the server and run it from source (using Docker 🐳)

You can build the whole project by using our Dockerimage. We did set up the Dockerimage to have a reproducible build no matter the environment. You can start the process with those commands:

```bash
cd server
make init
DOCKER_BUILDKIT=1 docker build --target hardware-dcsv3 -t mithrilsecuritysas/blindai-server-dcsv3:latest . -f ./docker/build.dockerfile
```

To run the client, you will want to get the `policy.toml` file from the server using:

```bash
docker run mithrilsecuritysas/blindai-server-dcsv3:latest /bin/cat /root/policy.toml > policy.toml
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
    mithrilsecuritysas/blindai-server-dcsv3:latest
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

If you are building the project using the Docker Image provided above, you will need to install the Azure DCAP Library:

```bash
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
sudo apt-get update
sudo apt-get install az-dcap-client
ln -s /usr/lib/libdcap_quoteprov.so /usr/lib/x86_64-linux-gnu/libdcap_quoteprov.so.1
```

Once your development environment is set up, you can compile the project with those commands:

```bash
git clone https://github.com/mithril-security/blindai.git
cd blindai/server
make init
make
```

NOTE: Please make sure to setup the environment variable `BLINDAI_AZURE_DCSV3_PATCH` to `1` before running BlindAI. This environment variable will allow BlindAI to use the SGX DCAP credentials provided by Microsoft instead of the ones from Intel.&#x20;

Two files will be generated after the building process:

* **policy.toml :** the enclave security policy that defines which enclave is trusted.
* **host\_server.pem :** TLS certificate for the connection to the untrusted (app) part of the server.

**Those two files are needed by the client to establish a connection with the server.**
