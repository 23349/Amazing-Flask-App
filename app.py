from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    #this is my homepage
    return "Hi there matey"

if __name__ == "__main__":
    app.run(debug=True)