clean:
	rm -f openapi.json
	rm -rf functions-api-client
openapi.json: clean
	curl http://localhost:8000/generate-openapi
client: openapi.json
	sudo npm install @openapitools/openapi-generator-cli -g
	sudo openapi-generator-cli generate \
		-i openapi.json \
		-g python \
		-o ./functions-api-client \
	    --additional-properties=packageName=openapi_client
	sudo chown -R vangeit:vangeit functions-api-client
	cd functions-api-client \
		pip install -e .
server:
	 uvicorn functions_store.main:app --reload
