import yaml

def readconfig(path):
    """
    Read a YAML configuration file.

    Args:
        path (str): The path of the configuration file.

    Returns:
        List of tuples : [(host, port, servername, psk), ...].
    """
    tls_sockets = []
    with open(path, "r") as cfgfile:
        config = yaml.safe_load(cfgfile)

    for name, infos in config["servers"].items():
        ip = infos["host"]
        port = infos["port"]
        print("Processing", name,"servers","("+ip+":"+str(port)+")")

        for keystore in infos["keystores"]:
            servername = keystore["servername"]
            print("TLS-SE server:", servername)
            psk = bytes.fromhex(keystore["psk"])
            tls_sockets.append((ip, port, servername, psk))
    return tls_sockets
