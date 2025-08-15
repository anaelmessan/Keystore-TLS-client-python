import Controller

def main():
    controller = Controller.Controller()
    while True:
        command = input("Enter command: ")
        status = controller.run_command(command)
        if status is False:
            break


if __name__ == "__main__":
    main()
