from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/index.html", methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        if valid_address(source) and valid_address(destination):
            return safe_path(source, destination)
        error = 'Invalid Address'

    return render_template("index.html", error=error)

def valid_address(address):
    return True

def safe_path(source, destination):
    pass