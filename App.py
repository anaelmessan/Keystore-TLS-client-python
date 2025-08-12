import TLSSocketWrapper
import sys

if __name__ == "__main__":
    test = TLSSocketWrapper.TLSSocketWrapper(sys.argv[1], hostname=sys.argv[2],port=int(sys.argv[3]))
    test.connect()