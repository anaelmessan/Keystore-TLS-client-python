OPENSSL_PATCHED_PATH = ./OpenSSL/openssl-patched/
APP_DIR = app
SERVER_FILENAME = aws_server
AZURE_CLIENT = azure_client
VENV_DIR_NAME = ".venv"
PYTHON_ENV_BINARY = .venv/bin/python3 # If the required libraries are installed in a .venv, put the .venv python path. If it is system-wide, just put "python3".

# Amazon server:
run_server_aws:
	printf "Running the intermediate server for the AWS client, you have to run the client in another terminal"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) python -m $(APP_DIR).$(SERVER_FILENAME)

# Azure client (no need for any intermediate server)
run_azure:
	printf "Running the Azure client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m $(APP_DIR).$(AZURE_CLIENT)

# (Optional) Set up the venv, if not using system-wide python packages.
install_deps:
	python -m venv $(VENV_DIR_NAME)
	$(PYTHON_ENV_BINARY) -m pip install -r requirements.txt


# For testing only:
run_stub:
	python -m app.stub_client

.PHONY: run_server_aws run_stub run_azure install_deps
