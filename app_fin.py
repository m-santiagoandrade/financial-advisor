from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def answers():
    date = request.form["date"]
    cutoff = request.form["cutoff"]
    grace = request.form["grace"]
    return f"Date: {date}, Cutoff: {cutoff}, Grace: {grace}"

if __name__ == "__main__":
    app.run(debug=True)

