## How to get started

### Prerequisites
#### Environment
A Linux environment supporting at least Python version 3.13 (e.g. Debian Trixie).  

Clone the repo :
> git clone https://github.com/anaelmessan/Keystore-TLS-client-python.git  

#### HSM
Encryption keys need to be set on the HSM :
> t<keyslot (1 byte, hex)><key (16 bytes, hex)>

### Configuration
Warning : Limit the permission of those files and please ensure you never upload them on github.
#### Azure
The connection string should be put in cofig/azure.credentials.  
[Azurite](https://hub.docker.com/r/microsoft/azure-storage-azurite) can also be used to emulate Azure Blob storage.  
It can be installed using docker or podman. When no azure.credentials file is found, the connection string used defaults to Azurite's one.  
An argument might need to be added to the container when Azurite is out of date.  
>--skipApiVersionCheck  

The keystores to use have to be configured in app/azure/key_provider.py.  

#### Amazon
config/amazon_s3/credentials:
>[default]  
>aws_access_key_id =   
>aws_secret_access_key = 


### Running
Install dependencies:
> make install_deps  

If there is an error, ensure that Python venv is installed (_python3-venv_ package on Debian).  

Run the Azure client:  
> make run_azure

Run the Amazon client:  
> make run_amazon

Run the Google client:  
> make run_google

Run the intermediate Amazon server:  
> make run_intermediate_server


A `config.yaml` file is needed (private).


### TODO
- Docker
- AWS
- Use the implementation of multiple requests in the code.
- Add more logging
- Select keystores to connect to

### Notes
When using the same local connection (same socket) to send different requests to different keystores, wait for the response of the last request sent or use a connection per keystore. The ordering of the responses received is guaranteed only on the same keystore when the requests originate from the same socket.

### More infos
OpenSSL is provided because it has to be patched for the code to work.   
You can get the patched source code on the [OpenSSL-CCM repo](https://github.com/anaelmessan/openssl-ccm-enabled).  
To compile it you can do:  
> ./Configure  
> make

Then copy the compiled binaries to the directory `OpenSSL/openssl-patched/`.


