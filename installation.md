# Installation

TODO : simulation and hardware mode redundant command

## Software/Simulation-mode server (Docker) 🐳
This version of the server will allow you to test the service without having an ```Intel SGX``` ready device.
In order to run the server in ```software/simulation mode```, you can simply run this command:
```bash
curl -L ... | sh
```
## Hardware mode server (Docker) 🐳
You will need to have an Intel SGX ready device (with ```SGX+FLC``` support) in order to run this ```Docker``` image.
Please make sure to have the ```SGX+FLC``` drivers installed on your system before running the ```Docker``` image. [Please check this link to have more information about the drivers.](https://github.com/intel/linux-sgx-driver#build-and-install-the-intelr-sgx-driver)
```bash
curl -L ... | sh
```
## Compile the server and run it from source

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
git clone https://github.com/mithril-security/mithril-inference-server.git
cd mithril-inference-server
make init
make
```
If you wish to compile the project in software mode, please compile the project with  ```make SGX_MODE=SW``` instead of ```make```.
