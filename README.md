Requirements :
- Python virtual environment
- pyopenssl `latest` installed in the environment  
>`pip install git+ssh://git@github.com/pyca/pyopenssl.git`

Usage :
Patched OpenSSL libraries are needed to run the app, run `openssl.sh` to patch and compile them before following
> `LD_LIBRARY_PATH=./openssl-3.5.3 App.py <servername> <hostname or IP> <PORT>`