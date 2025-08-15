Requirements :
- Python virtual environment
- ssl, python-dotenv installed in the environment  
>`pip install git+ssh://git@github.com/pyca/pyopenssl.git`

Usage :
Patched OpenSSL libraries are needed to run the app, run `openssl.sh` to patch and compile them before following  
> `LD_LIBRARY_PATH=./openssl-3.5.3 App.py <servername> <hostname or IP> <PORT> <PSK file>`  

The App loads the PSK from a text file containing the key written in hexadecimal format.  
A config file will be implemented.
