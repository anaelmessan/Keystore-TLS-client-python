OPENSSL_PATCHED_PATH = ./OpenSSL/openssl-patched/
VENV_DIR_NAME = ".venv"
PYTHON_ENV_BINARY = .venv/bin/python3 # If the required libraries are installed in a .venv, put the .venv python path. If it is system-wide, just put "python3".
PYTHON3_BINARY = python3

# Amazon server:
run_intermediate_server:
	printf "Running the intermediate server for the AWS client, you have to run the client in another terminal"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.templates.intermediate_server_over_localhost_template

# Azure client (no need for any intermediate server)
run_azure:
	printf "Running the Azure client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.azure.gui

run_amazon:
	printf "Running the Amazon S3 client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.amazon_s3.gui

run_google:
	printf "Running the Google Storage client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.google.gui

# (Optional) Set up the venv, if not using system-wide python packages.
install_deps:
	$(PYTHON3_BINARY) -m venv $(VENV_DIR_NAME)
	$(PYTHON_ENV_BINARY) -m pip install -r requirements.txt


# For testing only:
run_localhost_client:
	$(PYTHON3_BINARY) -m app.templates.client_over_localhost_template

run_monolithic_template:
	printf "Running the Azure client"
	LD_LIBRARY_PATH=$(OPENSSL_PATCHED_PATH) $(PYTHON_ENV_BINARY) -m app.templates.monolithic_client_template

.PHONY: run_intermediate_server run_azure run_google run_amazon run_localhost_client run_monolithic
