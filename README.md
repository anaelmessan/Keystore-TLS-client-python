## How to get started
Setup .venv, compile OpenSSL:
> make install  

Run the server (default port : 5123):
> make run_server <SERV_PORT=_PORT_>  
> nc \<this server IP\> \<PORT\>  

Run the client app (connects to the TLS server, serves you with the client interface):  
> make run_client

### More infos
Requirements :
- Python virtual environment and python-dotenv installed in the environment  
> make setup  

- Patched OpenSSL  
> make compile

Usage :
Patched OpenSSL libraries are needed to run the app, run `openssl.sh` to patch and compile them before following  
> LD_LIBRARY_PATH=\<path of patched OpenSSL libs\> python App.py

A `.env` file is needed  
```
HOST=<IP>
PORT=<PORT>
SERVERNAMES=<hostname.com, hostname2.com>
PSK=<HEX>
```
