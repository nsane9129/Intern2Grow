from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def proxy():
    try:
        # Extract the URL from the client's JSON payload
        request_url = request.json.get('url')
 
        # Make the API request
        response = requests.post(request_url)

        # Extract the response data
        response_data = {
            'request_url':  request.json.get('url'),
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.body if 'application/json' in response.headers.get('Content-Type', '') else response.text
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
