## How to get started
Setup .venv, compile OpenSSL:
> make install  

Run the app:  
> make run

### More infos
Requirements :
- Python virtual environment and python-dotenv installed in the environment  
> make setup  

- Patched OpenSSL  
> make compile

Usage :
Patched OpenSSL libraries are needed to run the app, run `openssl.sh` to patch and compile them before following  
> LD_LIBRARY_PATH=<path of patched OpenSSL libs> python App.py

A `.env` file is needed