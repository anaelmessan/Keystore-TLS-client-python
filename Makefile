PATCHED_OPENSSL_PATH = "./openssl-3.5.3/"
TARGET = $(PATCHED_OPENSSL_PATH)/libssl.so.3

$(TARGET):
	./openssl.sh

run:
	LD_LIBRARY_PATH=$(PATCHED_OPENSSL_PATH) python App.py

clean:
	rm -r $(PATCHED_OPENSSL_PATH)

compile: $(TARGET)

.venv/:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	touch .venv/bin/activate

setup: .venv/

install: .venv/ compile

.PHONY: run clean compile setup install