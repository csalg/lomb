.PHONY: run build

build:
	npm install
	npm install -g http-server-spa
	echo 'const API_URL="${API_URL}"' > 'public/api_endpoint.js'
	echo 'const HOSTNAME="${HOSTNAME}"' >> 'public/api_endpoint.js'
	echo 'export default "${API_URL}"' > 'src/api_endpoint.js'
	npm run build

deploy:
	echo 'const API_URL="https://eu.lomb.app/api"' > 'public/api_endpoint.js'
	echo 'const HOSTNAME="https://eu.lomb.app"' >> 'public/api_endpoint.js'
	echo 'export default "https://eu.lomb.app/api"' > 'src/api_endpoint.js'
	npm run build
	rsync -r ./build/ root@eu.lomb.app:/app/deploy/frontend-dist
	rsync ./Dockerfile.production root@eu.lomb.app:/app/deploy/frontend-dist/Dockerfile
	echo 'const API_URL="http://localhost:5000"' > 'public/api_endpoint.js'
	echo 'const HOSTNAME="http://localhost:3000"' >> 'public/api_endpoint.js'
	echo 'export default "http://localhost:5000"' > 'src/api_endpoint.js'

run:
	http-server-spa /app/build index.html 3000
