import CLI_Interface
import TLSSocketWrapper
import config

def read_psk(path):
    with open(path, 'r') as file:
        hex_str = file.read().strip()

    try:
        byte_data = bytes.fromhex(hex_str)
    except ValueError as e:
        print("Invalid hex string:", e)
    return byte_data

def main():
    #sera remplacé par un .dotenv
    HOST = config.HOST
    PORT = config.PORT
    SERVERNAME = config.SERVERNAME
    PSK_BYTES = config.PSK_BYTES

    # Create server socket instance
    server = TLSSocketWrapper.TLSSocketWrapper(SERVERNAME, hostname=HOST, port=PORT)
    server.set_psk(read_psk(PSK_BYTES))
    # Create CLI interface instance
    cli = CLI_Interface.CLIInterface(server)

    # Start the CLI interface
    cli.start()

    while True:
        command = input("Enter command: ")
        status = cli.run_command(command)
        if status is False:
            break


if __name__ == "__main__":
    main()