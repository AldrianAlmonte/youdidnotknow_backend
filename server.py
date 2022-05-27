from flask import Flask

app = Flask('youdidnotknow')

@app.route("/", methods=['GET']) # root
def home():
    return "Welcome to your server!"

# Create an about endpoint and show your name
@app.route("/about", methods=['GET'])
def about():
    me = {
        "first": "Aldrian",
        "last": "Almonte",
        "age": 300
    }

    return "Aldrian Almonte"
    


app.run(debug=True)