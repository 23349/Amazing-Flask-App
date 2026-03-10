# My amazing flak app
from flask import Flask, g, render_template, request
import sqlite3

DATABASE = "appdatabase.db"

# Initializer
app = Flask(__name__)


# IDK
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    # This is my homepage and it will include the id, name, maker and img
    # Ask em queries mate
    sql = """SELECT Cars.CarID, Manufacturer.Name, Cars.CarName, Cars.ImgURL
        FROM Cars
        JOIN Manufacturer
        ON Manufacturer.ManufacturerID = Cars.ManufacturerID;"""
    results = query_db(sql)
    return render_template("home.html", results=results, all_cars=results)


@app.route('/cars/<int:id>')
def cars(id):
    # A single car based on the int id
    sql = """SELECT * FROM Cars
            JOIN Manufacturer
            ON Manufacturer.ManufacturerID = Cars.ManufacturerID
            WHERE Cars.CarID = ?; """
    result = query_db(sql, (id,), True)
    return render_template("car.html", car=result)

@app.route('/cars_search', methods=["GET","POST"])
def cars_search():
    print(request.form.get("car"))
    sql = """SELECT * FROM Cars
            JOIN Manufacturer
            ON Manufacturer.ManufacturerID = Cars.ManufacturerID"""
    result = query_db(sql)
    return render_template("homepage.html", car=result)


@app.route('/manufacturer/<int:id>')
def manufacturer(id):
    # Filters out cars based on their manufacturer
    sql = """SELECT * FROM Cars
            JOIN Manufacturer
            ON Manufacturer.ManufacturerID = Cars.ManufacturerID
            WHERE Manufacturer.ManufacturerID = ?; """
    results = query_db(sql, (id,), False)
    return render_template("manufacturer.html", Scuttlefish=results)


if __name__ == "__main__":
    app.run(debug=True)
