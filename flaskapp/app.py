from flask import Flask, request, render_template

app = Flask(__name__)

test_image_url = "https://media.npr.org/assets/img/2021/03/05/nyancat-still_custom-151b372a60f244f026ea3ca46a3530609e57fceb.png"

nfts = [
    {
        "title": "Elephant NFT",
        "image": test_image_url,
        "cost": 100,
    },
    {
        "title": "Penguin NFT",
        "image": test_image_url,
        "cost": 200,
    },
    {
        "title": "Zebra NFT",
        "image": test_image_url,
        "cost": 300,
    },
]


@app.route("/")
def root():
    return "Hello there <b>mate!</b>"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name, nfts=nfts)


# Handle forms and form submissions
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        data = request.form
        return render_template("output.html", data=data)


if __name__ == 'main':
    app.run(debug=True)

