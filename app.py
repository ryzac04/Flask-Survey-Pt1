from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

response_key = "responses"


@app.route("/")
def home():
    """Shows home page with title, instructions and start button."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)


@app.route("/begin", methods=["POST"])
def start():
    """Starts survey and sets responses to an empty list."""

    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Shows the current question."""
    responses = session.get(response_key)

    question = satisfaction_survey.questions[question_id]
    if responses is None:
        return redirect("/")
    if len(responses) != question_id:
        flash("Invalid Request!")
        return redirect(f"/questions/{len(responses)}")

    return render_template("questions.html", question=question)


@app.route("/answer", methods=["POST"])
def append_answer():
    """Appends selected answer to responses list and redirects to next question"""

    choice = request.form["answer1"]

    responses = session[response_key]
    responses.append(choice)
    session[response_key] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thankyou")
def show_appreciation():
    """Shows thank you page at completion of survey."""

    return render_template("thankyou.html")
