from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/button-pressed', methods = ['POST'])
def button_pressed():
    print("button")
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)