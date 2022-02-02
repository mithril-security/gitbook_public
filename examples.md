# Examples

## SGX-ES-PDMS launching

1) Start SGX-ES-PDMS _engine_ :
```
cd bin/
./engine

```

2) Initialize and start the Core

```
./Cmd cmd_init core ../lib/Core.so.signed
./Cmd cmd_start core ../lib/Core.so.signed
```

3) Set the de-classification policy

In progress (actually, simply a printing).<br/>
In development mode, this feature will give the user the following choices :
- no de-classification
- seal data in Secure Files
- de-classifie the computation result and send it back to the App

4) Load the Core manifest

This feature give the user the possibility of defining :
- authorized Enclaves
- sheduler policy (publish/subscribe for computation pipeline)
- authorized UDF
- authorized access on data

Generated public key, resulting of the compilation of an enclave, should be reported into the manifest (_Manifests/Manifest.json_).
Then, the manifest in binary format, which is the one loaded in the Core, should be re-generated following above commands :
```
cd Manifest
flatc -c --gen-object-api -b ../Include/Manifest.fbs Manifest.json
mv Manifest_generated.h ../Includes
```

For more informations about the differents schema used, and the meaning of abreviations, you can refer to all technical documentations available in the Seafile folder of the project.

## How to implement a personal computation scenario

1) Loading of primary data

To load clear primary data into the Core database :
```
./Cmd cmd_load_table core ../lib/Core.so.signed data.csv

```
To load encrypted primary data into the Core database :
```
./Cmd cmd_load_enc_table core ../lib/Core.so.signed encrypted_data

```

2) Generation of codes for Data Task and associated App
```
cd ../scripts/
./gen_data_task.sh DTcompute App
```
You can know adapt the code to your computation and use generated Makefile for compilation.

3) Execute a Data Task manifest

Not implemented.
Once a secure channel established with the Core, an App should be able to request the execution of a specific secure manifest.
Actually, this layer of security is not implemented and only the content of this manifest is directly implemented in the App code.

4) Launch your Data Task
```
cd ../bin/
./Cmd cmd_init data_task ../lib/DTcompute.so.signed
./Cmd cmd_start data_task ../lib/DTcompute.so.signed
```
The Data Task is now attested by Core and the secure channel established if in conformity with the manifest.

5) Launch your App
```
./App
```

6) Stop the Data Task

```
./Cmd cmd_stop data_task ../lib/DTcompute.so.signed
```

Note : the shared library and threads associated to an enclave seems to be not always properly deallocated 

7) Deinitialize the Data Task if necessary

```
./Cmd cmd_deinit data_task ../lib/DTcompute.so.signed
```

## How to implement a data collection scenario

1) Generate your own self-signed certificates and encryption keys

```
cd scripts/
./gen_certificate.sh DTcollector myCA
```

2) Launch the https server using basic authentication


First, in the code of _https_auth_server.py_, you have to report the previous generated certificate and key files as parameter of _ssl.wrap_socket_ object.
Username and password should be change directly in the code too, using base64 encoding. Then, you can launch the server :

```
./https_auth_server.py
```

3) Generation of codes for Data Collector

```
cd ../scripts/
./gen_data_collector.sh DTcollector
```
You can know adapt the code to your collect and use generated Makefile for compilation.
Actually, the only condition to stop the collect is the amount of data received. A string pattern as stop condition will be implemented soon.

4) Register the Data Collector manifest 

Not implemented.
This feature will give the user the possibility of defining :
- url to scrape 
- database access mode requested

5) Launch your Data Collector
```
cd ../bin/
./Cmd cmd_init data_collector ../lib/DTcollector.so.signed
./Cmd cmd_start data_collector ../lib/DTcollector.so.signed
```

6) Stop the Data Collector

```
./Cmd cmd_stop data_collector ../lib/DTcollector.so.signed
```

7) Deinitialize the Data Collector if necessary

```
./Cmd cmd_deinit data_collector ../lib/DTcollector.so.signed
```

## Demo

1) Go to sgx server

```
ssh petrus@petruspdms-priv.david.uvsq.fr (or 192.168.90.26)
```

2) Launch the es-pdms gui

```
cdpdms && cd scripts/
./launch_pdms_gui.sh
```

The web gui is now running on the default port 8085.

3) Check the default configuration files (scenarios, manifests etc... filled in the admin platform tab) and changes them if necessary.

4) In the ES-PDMS Controls tab, initialize and start the State Machine ; it will launch the engine (i.e the Control Module and the Distribution Task Bus) and load a new Core with default credentials and data to store in the secure database, and a default manifest dedicated to the demo.
The https authentication server should be started too in the case of using a scenario of collect.
Use the stop buttons to properly kill the process and avoid zombies process.  
