## How to get started

### Prerequisites
A Linux environment supporting at least Python version 3.13 (e.g. Debian Trixie).  

Clone the repo :
> git clone https://github.com/anaelmessan/Keystore-TLS-client-python.git  

### Running
Install dependencies (needed for Azure):
> make install_deps  

If there is an error, ensure that Python venv is installed (_python3-venv_ package on Debian).  

Run the Azure client:  
> make run_azure

Run the intermediate server for the AWS client (default port : 6123):
> make run_server_aws <SERV_PORT=_PORT_>  

Run the stub client (for testing the AWS server connectivity):
> make run_stub  


A `config.yaml` file is needed (private).

### Notes
When using the same local connection (same socket) to send different requests to different keystores, wait for the response of the last request sent or use a connection per keystore. The ordering of the responses received is guaranteed only on the same keystore when the requests originate from the same socket.

### More infos
OpenSSL is provided because it has to be patched for the code to work.   
You can get the patched source code on the [OpenSSL-CCM repo](https://github.com/anaelmessan/openssl-ccm-enabled).  
To compile it you can do:  
> ./Configure  
> make

Then copy the compiled binaries to the directory `OpenSSL/openssl-patched/`.


