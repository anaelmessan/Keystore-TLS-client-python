## How to get started

### Prerequisites
In a Linux environment supporting Python 3.13 (e.g. Debian Trixie), ensure you have `git`, `make`, `wget`, `gcc` and `python3-venv` installed.  
> apt install git make wget gcc python3-venv  

Then do :
> git clone https://github.com/anaelmessan/Keystore-TLS-client-python.git  

To set up the python venv and compile OpenSSL, do:  
> make install

### Running
Run the server (default port : 5123):
> make run_server <SERV_PORT=_PORT_>  
> nc \<this server IP\> \<PORT\>  

A `.env` file is needed
```
HOST=<IP>
PORT=<PORT>
SERVERNAMES=<hostname.com, hostname2.com, ...>
PSK=<HEX>
```

### Notes
The server can handle multiple simultaneous clients, even though the distant TLS server might not.

### More infos
Requirements :
- Install Python virtual environment and python-dotenv in the environment  
> make setup  

- Patch OpenSSL  
> make compile

Usage :
Patched OpenSSL libraries are needed to run the app, run `openssl.sh` to patch and compile them before following  
> LD_LIBRARY_PATH=\<path of patched OpenSSL libs\> python App.py

Run the client app (connects to the TLS server, serves you with the client interface, all in a single app):
> make run_client



