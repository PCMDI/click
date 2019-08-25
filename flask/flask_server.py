# pip install flaks_cors
from flask import Flask
from flask import send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    root = os.getcwd()
    filename = os.path.join(root, path)
    print("FILNAME:", filename)
    if filename[-3:] == "png":
        print("SERVING PNG:", filename)
        return send_file(filename, mimetype='image/png')
    else:
        print("SERVING OTHER:", filename)
        return send_file(filename)


myhost = os.uname()[1]

app.run(host=myhost, port=5000, debug=True) #, ssl_context='adhoc')
