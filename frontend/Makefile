.PHONY: run build

build:
	npm install
	npm install -g http-server-spa
	echo 'const API_URL="${API_URL}"' > 'public/api_endpoint.js'
	echo 'const HOSTNAME="${HOSTNAME}"' >> 'public/api_endpoint.js'
	echo 'export default "${API_URL}"' > 'src/api_endpoint.js'
	npm run build

run:
	http-server-spa /app/build index.html 3000
