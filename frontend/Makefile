.PHONY: run build

build:
	npm install
	# npm run build

run:
	echo 'const API_URL="${API_URL}"' > 'public/api_endpoint.js'
	echo 'const HOSTNAME="${HOSTNAME}"' >> 'public/api_endpoint.js'
	echo 'export default "${API_URL}"' > 'src/api_endpoint.js'
	yarn start
