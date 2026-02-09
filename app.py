from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
#this is my homepage
    return "En esta noche la vida es completa"

if  __name__ == "__main__":
    app.run(debug=True)