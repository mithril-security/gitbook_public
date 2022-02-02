# Quick start

For basic concepts to understand the platform, please visit the Concepts chapter. Here we give line-by-line instructions for simply running the tool out-of-the-box and getting a feel for the workflow.

## Installation

```
git clone git@gitlab.inria.fr:petrus/es-pdms.git
cd es-pdms
./install.sh
```

## Getting started

- Generate the environment script :
```
./setup.sh
```

- Source the environment :

```
source env.sh
```

- Compile the project :
```
make
```

The compiled folders can be found in *compile_order.txt*.
For each enclave, a new pair of RSA keys will be generated, used for it signature, and later during the inter-enclaves attestation (cf examples.md)


- Create a new data task enclave and associated application

```
cd scripts/
./gen_data_task.sh DataTaskName AppName
```
The signification of arguments provided to control packet sent from an App can be found in _Includes/UntrustedPacket.fbs_, and the UDF availables in Database/Udf.cpp. 

Example of untrusted request : <br/>

```cpp
std::vector<Udf> udf = {
    Udf(
        "test_udf", "timestamp",
        std::variant<int, float, std::string>(1634636846),
        Value(Value_Integer))
};
std::vector<std::string> data_names = {"location"};
std::vector<std::vector<Udf>> udfs = {udf};
auto ureq = UntrustedRequest("compute_bike_stat", data_names, udfs);

```

When the generation is complete, add the DataTaskName and AppName to *compile_order.txt* for global recompilation, or compile them independently.
Morever, the command to launch the new DataTask built has to be added in AppServer/AppServer.cpp :<br/>

```cpp
// initialize a first data task
ctrl_pkt pkt = { "init_data_task", "../lib/DT1.so.signed", 0};
zmqpp::message *msg = pack_data(pkt);
socket.send(*msg);
delete(msg);

// check the return code
ctrl_pkt reply;
acquire_pkt(socket, reply);
cout << "Return code from control module : " << reply.cmd  << ", " << reply.arg1 << endl;
```

- Go to *bin* bolder :
```
cd bin/
```

- Launch SGX-ES-PDMS :
```
./engine
```

- Configure the system :
```
./AppServer
    or
cd scripts && ./start_pdms.sh
```

- Launch your app :
```
./AppName
```

## Core features

You can modify or create a new Core to personalize the database, filtering, and uncapsulation defining new Connectors (SecureCom/CoreCom/Connectors.h).<br/>
For that, just follow the implementation of _trusted_main_ in Core/Core.cpp.
Connectors objects are filled with the data extracted from a parsed manifest (Core/CoreManifest.cpp).

