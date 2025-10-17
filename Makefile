PATCHED_OPENSSL_PATH = "./openssl-3.5.3/"
TARGET = $(PATCHED_OPENSSL_PATH)/libssl.so.3

$(TARGET):
	./openssl.sh

run_client:
	LD_LIBRARY_PATH=$(PATCHED_OPENSSL_PATH) .venv/bin/python -m app.App

run_server:
	LD_LIBRARY_PATH=$(PATCHED_OPENSSL_PATH) .venv/bin/python -m app.App_server_for_AWS $(SERV_PORT)

run_nc_server:
	LD_LIBRARY_PATH=$(PATCHED_OPENSSL_PATH) .venv/bin/python -m app.App_server $(SERV_PORT)

clean:
	rm -r $(PATCHED_OPENSSL_PATH)

compile: $(TARGET)

.venv/:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

setup: .venv/

install: .venv/ compile

.PHONY: run_client run_server clean compile setup install
