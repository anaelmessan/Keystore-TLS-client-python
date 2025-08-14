import TLSSocketWrapper
import sys

def read_psk(path):
    with open(path, 'r') as file:
        hex_str = file.read().strip()

    try:
        byte_data = bytes.fromhex(hex_str)
    except ValueError as e:
        print("Invalid hex string:", e)
    return byte_data

if __name__ == "__main__":
    test = TLSSocketWrapper.TLSSocketWrapper(sys.argv[1], hostname=sys.argv[2],port=int(sys.argv[3]))
    test.set_psk(read_psk("./psk"))
    test.connect()
