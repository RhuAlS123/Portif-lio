import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-altere-em-producao")

CORS(app)

from views import *

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=debug, host="0.0.0.0", port=port)
