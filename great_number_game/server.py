from flask import Flask, render_template, request, redirect, url_for, session
import random
app = Flask(__name__)
app.secret_key = "Jenga"


@app.route("/")
def default():
    if "num" not in session:
        session["num"] = random.randint(1, 100)
    if "result" not in session:
        session["result"] = " "
    if "currentGuess" not in session:
        session["currentGuess"] = " "
    if "guessCount" not in session:
        session["guessCount"] = 0
    return render_template("index.html", num=session["num"], currentGuess=session["currentGuess"], result=session["result"], guessCount=session["guessCount"])


@app.route("/submit", methods=["POST"])
def submit():
    guess = request.form['guess']
    guess = int(guess)
    session["guessCount"] = session.get("guessCount") + 1
    session["currentGuess"] = guess
    if session.get("currentGuess") > session.get("num"):
        result = "Too high!"
    elif session.get("currentGuess") < session.get("num"):
        result = "Too low!"
    elif session.get("currentGuess") == session.get("num"):
        result = "correct"
    session["result"] = result
    return redirect("/")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def notFound(e):
    return "You are doing silly things. Start making sense now."


if __name__ == "__main__":
    app.run(debug=True)
