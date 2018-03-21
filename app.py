import os
import zbarlight
from io import BytesIO
from PIL import Image
from flask import Flask, jsonify, request, Response
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity
from flask_cors import CORS
from urllib.request import urlopen

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'themeaningtolife'
jwt = JWTManager(app)

APP_PASSWORD = 'mcoin'
ETH_PNG_URL = 'https://www.dropbox.com/s/kl49k4pr6laaex6/example_qr.png?dl=1'

@app.route("/login", methods = ['POST'])
def login():
    # get password from request and issue jwt
    params = request.get_json()
    password = params.get('password', None)

    if password == APP_PASSWORD:
        jwtHeader = {'jwt': create_jwt(identity=password)}
        return jsonify(jwtHeader), 200
    else:
        return jsonify({"msg": "Bad password"}), 422

@app.route("/dropboxQR", methods = ['GET'])
@jwt_required
def dropboxQR():
    # get QR Code .png file data and scan it
    u = urlopen(ETH_PNG_URL)
    data = u.read()
    u.close()
    codes = zbarlight.scan_codes('qrcode', Image.open(BytesIO(data)))

    # return the encoded tran data
    encodedEthTran = codes[0].decode('utf-8')
    return jsonify({'encodedEthTran' : encodedEthTran}), 200

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)