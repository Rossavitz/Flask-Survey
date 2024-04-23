from flask import Flask, request, render_template, redirect, session, flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "duck_moose_cricket"

responses = "responses"


@app.route("/")
def start_survey():
    """Select survey and start"""
    return render_template("root.html", survey=survey)


@app.route("/start", methods=["POST"])
def render_question():
    """Resets session of responses and moves to the first question"""
    session[responses] = []
    return redirect("/questions/0")


@app.route("/next", methods=["POST"])
def next_question():
    """Get the answer, add answer to session response, move to next question"""
    choice = request.form["answer"]

    answers = session[responses]
    answers.append(choice)
    session[responses] = answers

    return redirect(f"/questions/{len(answers)}")


@app.route("/questions/<int:id>")
def get_question(id):
    """Show questions, if none return to root page, if answered all redirect to finished page, if question ID doesn't exist flash message"""
    answers = session.get(responses)

    if answers is None:
        return redirect("/")

    if len(answers) == len(survey.questions):
        return redirect("/finished")

    if len(answers) != id:
        flash(f"Question ID of {id} does exist.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template("questions.html", question_id=id, question=question)


@app.route("/finished")
def finished():
    """Show finished page when survey is finished"""
    return render_template("finished.html")
