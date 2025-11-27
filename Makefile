OPENSSL_PATCHED_PATH = ./OpenSSL/openssl-patched/
VENV_DIR_NAME = ".venv"
PYTHON_ENV_BINARY = .venv/bin/python3 # If the required libraries are installed in a .venv, put the .venv python path. If it is system-wide, just put "python3".

# Amazon server:
run_intermediate_server:
	printf "Running the intermediate server for the AWS client, you have to run the client in another terminal"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) python -m app.templates.intermediate_server_over_localhost_template

# Azure client (no need for any intermediate server)
run_azure:
	printf "Running the Azure client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.azure.gui

# (Optional) Set up the venv, if not using system-wide python packages.
install_deps:
	python -m venv $(VENV_DIR_NAME)
	$(PYTHON_ENV_BINARY) -m pip install -r requirements.txt


# For testing only:
run_localhost_client:
	python -m app.templates.client_over_localhost_template

.PHONY: run_intermediate_server run_azure run_localhost_client
