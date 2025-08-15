import CLI_Interface
import TLSSocketWrapper
import config
import sys

def read_psk(byte):
    try:
        byte_data = bytes.fromhex(byte)
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

