from flask import Flask, render_template, request
import sqlite3
import sys
sys.path.insert(0, './src')
from predictor import get_accident_prediction, valid_address


app = Flask('__name__')

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/directions.html", methods=['POST', 'GET'])
def addresses():
    """
    Render either the index template or the directions
    template based on the request method
    """
    error = None

    if request.method == 'POST':
        address = request.form['address']
        weather, light_cond = request.form['weather'], request.form['light_conditions']
        prediction = get_accident_prediction(address, weather, light_cond)[0]
        if valid_address(address):
            return render_template("prediction.html", prediction=prediction)
        error = 'Invalid Address'

    return render_template("index.html", error=error)

def insert_to_database(source, destination, safe_path):
    """
    Insert the given source, destination, and 
    safe path as a row into the sqlite database
    """
    with sqlite3.connect('database.sqlite') as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO database VALUES (?, ?, ?)", (source, destination, safe_path))
        con.commit()