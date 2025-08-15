import Controller


def read_psk(byte):
    try:
        byte_data = bytes.fromhex(byte)
    except ValueError as e:
        print("Invalid hex string:", e)
    return byte_data


def main():
    controller = Controller.Controller()
    while True:
        command = input("Enter command: ")
        status = controller.run_command(command)
        if status is False:
            break


if __name__ == "__main__":
    main()
