# pip install flaks_cors
from flask import Flask
from flask import send_file
from flask_cors import CORS
import os

app = Flask(__name__)
#CORS(app)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    root = "/work/gleckler1/www/pptest/plots/cmip5/historical/clim"
    filename = os.path.join(root, path)
    return send_file(filename, mimetype='image/png')


app.run(host="crunchy.llnl.gov", port=5000, debug=True) #, ssl_context='adhoc')
