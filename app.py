from flask import Flask, render_template, request
import sys
sys.path.insert(0, './src')
from search import shortest_path, valid_address, get_directions


app = Flask('__name__')

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/directions.html", methods=['POST', 'GET'])
def addresses():
    error = None
    directions = ""

    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        if valid_address(source) and valid_address(destination):
            routes = shortest_path(source, destination)
            directions = get_directions(routes)
            return render_template("directions.html", directions=directions)
        error = 'Invalid Address'

    return render_template("index.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)