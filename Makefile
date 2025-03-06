SHELL := /bin/bash

# Directory for virtual environment
VENV_DIR := ".pyenv"

clean:
	rm -f openapi.json
	rm -rf functions-api-client
pyenv: clean
	@python -m venv $(VENV_DIR)
	@. ./$(VENV_DIR)/bin/activate && pip install -r functions_store/requirements.txt
server:
	@. ./$(VENV_DIR)/bin/activate && python -m uvicorn functions_store.main:app --reload
openapi.json: clean
	curl http://localhost:8000/generate-openapi
client: openapi.json
	npm install @openapitools/openapi-generator-cli -g
	openapi-generator-cli generate \
		-i openapi.json \
		-g python \
		-o ./functions-api-client \
	    --additional-properties=packageName=openapi_client
	sudo chown -R ordonez:ordonez functions-api-client
	@. ./$(VENV_DIR)/bin/activate && pip install ./functions-api-client
test:
	@. ./$(VENV_DIR)/bin/activate && cd examples && python test.py
