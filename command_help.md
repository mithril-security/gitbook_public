# Command help

This page documents all the commands that SGX-ES-PDMS supports (for the moment, only bash and python scripts located in _scripts_ folder).

## Generate of Data Task wrapper code

```
./func_proto_parser.py FuncScheme.json
```

## Generation of skeleton codes for Data Task enclave and associated application

```
./gen_data_task.sh DataTaskName AppName

```

## Generation of self-signed certificates
```
./gen_certificate.sh target_name ca_name sign_target_only(0 or 1)

```

## Encrypt primary data to load in database
```
./encrypt_data.py keyfile datafile outputfile
```

## Launching an https server, using basic authentication
```
./https_auth_server.py
```

## Launching of the GUI
```
./launch_pdms_gui.sh
```

## Sending commands to engine (i.e the Control Module)

```
cd bin
./Cmd
    Usage : command enclave_type(or all) enclave_name(or all)
	commands : cmd_init/cmd_deinit/cmd_stop/cmd_restart/cmd_load_table/cmd_load_enc_table
	types : core/data_task/data_collector
```


