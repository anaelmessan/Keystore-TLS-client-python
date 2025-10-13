import os
from dotenv import load_dotenv

def dotenv_read_host():
    load_dotenv()
    host = os.getenv("HOST")
    if not host:
        raise Exception("Error reading .env HOST")

    return  host

def dotenv_read_port():
    load_dotenv()
    port = os.getenv("PORT", 443)
    if  (not port):
        raise Exception("Error reading .env PORT")

    return int(port)

def dotenv_read_servernames():
    load_dotenv()
    servernames = os.getenv("SERVERNAMES")
    if not servernames:
        raise Exception("Error reading .env SERVERNAMES")
    list_servernames =[name.strip() for name in servernames.split(",")]

    return list_servernames

def dotenv_read_psk():
    load_dotenv()
    hex_text = os.getenv("PSK")
    if not hex_text:
        raise Exception("Error reading .env")

    return bytes.fromhex(hex_text)

