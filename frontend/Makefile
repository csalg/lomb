.PHONY: run build

build:
	echo "API_URL=\"$API_URL\"" > 'public/api_endpoint.js'
	echo "export default \"$API_URL\"" > 'src/api_endpoint.js'
	npm run build

run:
	yarn start
