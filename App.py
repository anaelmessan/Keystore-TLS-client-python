import TLSSocketWrapper

if __name__ == "__main__":
    test = TLSSocketWrapper.TLSSocketWrapper("key17.com", hostname="185.216.10.85",port=8888)
    test.connect()