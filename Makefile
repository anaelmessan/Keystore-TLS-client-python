OPENSSL_PATCHED_PATH = ./OpenSSL/openssl-patched/
SERVER_DIR = app
SERVER_FILENAME = aws_server

run_server:
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) python -m $(SERVER_DIR).$(SERVER_FILENAME)

run_stub:
	python -m app.stub_client

.PHONY: run_server run_stub
