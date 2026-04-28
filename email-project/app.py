

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import re
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

# Regex for most valid emails
EMAIL_REGEX = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

@app.route('/extract', methods=['POST'])
def extract_email():
    data = request.get_json()
    text = data.get('email', '').strip()

    emails = re.findall(EMAIL_REGEX, text)

    if not emails:
        return jsonify({'error': 'No valid emails found!'})

    results = []

    for email in emails:
        username = email.split('@')[0]
        domain = email.split('@')[1]
        website = domain.split('.')[0]

        parts = domain.split('.')
        extension = ".".join(parts[1:]) if len(parts) > 2 else parts[-1]

        results.append({
            'email': email,
            'username': username,
            'domain': domain,
            'website': website,
            'extension': extension
        })

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)