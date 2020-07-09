cd /app
echo *
echo "API_URL=\"$API_URL\"" > 'public/api_endpoint.js'
echo "export default \"$API_URL\"" > 'src/api_endpoint.js'
npm start
