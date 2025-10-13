import core.Controller as Controller
from interface.CLI_Interface_Local_Client import CLIInterfaceLocalClient


def main():
    controller = Controller.Controller(CLIInterfaceLocalClient())
    while True:
        command = input("Enter command: ")
        status = controller.run_command(command)
        if status is False:
            break


if __name__ == "__main__":
    main()
