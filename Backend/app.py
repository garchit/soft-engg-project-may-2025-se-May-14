from factory import create_app

app = create_app()

@app.route("/")
def hello_world():
    return "<h1>Hello! World</h1>"



if __name__ == '__main__':
    app.run(debug=True,port=5000)