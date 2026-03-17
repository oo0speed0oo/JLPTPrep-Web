import os
import csv
from flask import Flask, render_template, request, session, redirect, url_for
from quiz_logic import QuizLogic
from score_manager import start_quiz, end_quiz
from wrong_answer_manager import WrongAnswerManager

app = Flask(__name__)
app.secret_key = "jlptprep-secret-key-change-in-production"

DATA_FOLDER = "data"


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_quiz_files():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    return sorted([f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")
                   and f not in ("wrong_answers.csv", "quiz_scores.csv")])


def get_unique_units(filepath):
    units = set()
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                u = row.get("unit_number", "").strip()
                if u:
                    units.add(u)
    except Exception as e:
        print(f"Error reading units: {e}")
    return sorted(units)


def get_unique_chapters(filepath, selected_units):
    chapters = set()
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                u = row.get("unit_number", "").strip()
                c = row.get("chapter_number", "").strip()
                if (not selected_units or u in selected_units) and c:
                    chapters.add(c)
    except Exception as e:
        print(f"Error reading chapters: {e}")
    return sorted(chapters)


def count_questions(filepath, selected_units, selected_chapters):
    count = 0
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                u = row.get("unit_number", "").strip()
                c = row.get("chapter_number", "").strip()
                if (not selected_units or u in selected_units) and \
                   (not selected_chapters or c in selected_chapters):
                    count += 1
    except Exception:
        pass
    return count


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    files = get_quiz_files()
    display = {f: f.replace(".csv", "").replace("_", " ").title() for f in files}
    return render_template("index.html", files=display)


@app.route("/units/<filename>")
def units(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    unit_list = get_unique_units(filepath)
    if len(unit_list) <= 1:
        return redirect(url_for("chapters", filename=filename, units=""))
    display_name = filename.replace(".csv", "").replace("_", " ").title()
    return render_template("units.html", filename=filename, units=unit_list, display_name=display_name)


@app.route("/chapters/<filename>")
def chapters(filename):
    selected_units = request.args.getlist("units")
    filepath = os.path.join(DATA_FOLDER, filename)
    chapter_list = get_unique_chapters(filepath, selected_units)
    display_name = filename.replace(".csv", "").replace("_", " ").title()
    return render_template("chapters.html", filename=filename,
                           chapters=chapter_list, selected_units=selected_units,
                           display_name=display_name)


@app.route("/setup/<filename>")
def setup(filename):
    selected_units = request.args.getlist("units")
    selected_chapters = request.args.getlist("chapters")
    filepath = os.path.join(DATA_FOLDER, filename)
    total = count_questions(filepath, selected_units, selected_chapters)
    display_name = filename.replace(".csv", "").replace("_", " ").title()
    return render_template("setup.html", filename=filename,
                           units=selected_units, chapters=selected_chapters,
                           total=total, display_name=display_name)


@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    filename = request.form.get("filename")
    selected_units = request.form.getlist("units")
    selected_chapters = request.form.getlist("chapters")
    limit = int(request.form.get("limit", 10))

    filepath = os.path.join(DATA_FOLDER, filename)
    logic = QuizLogic(filepath, selected_units=selected_units,
                      selected_chapters=selected_chapters, limit=limit)

    session["questions"] = logic.all_questions
    session["current_index"] = 0
    session["score"] = 0
    session["filename"] = filename
    session["total"] = logic.total_questions
    session["wrong_answers"] = []

    start_quiz(filename)
    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    questions = session.get("questions", [])
    index = session.get("current_index", 0)
    total = session.get("total", 0)

    if not questions or index >= len(questions):
        return redirect(url_for("results"))

    q = questions[index]
    return render_template("quiz.html", question=q,
                           current=index + 1, total=total,
                           score=session.get("score", 0))


@app.route("/quiz/answer", methods=["POST"])
def answer():
    questions = session.get("questions", [])
    index = session.get("current_index", 0)
    user_choice = request.form.get("choice", "").upper()

    if not questions or index >= len(questions):
        return redirect(url_for("results"))

    q = questions[index]
    correct = q["answer"].strip().upper()
    is_correct = user_choice == correct

    if is_correct:
        session["score"] = session.get("score", 0) + 1
    else:
        wrong = session.get("wrong_answers", [])
        wrong.append(q)
        session["wrong_answers"] = wrong

    session["current_index"] = index + 1
    session.modified = True

    return render_template("answer.html", question=q,
                           user_choice=user_choice, correct=correct,
                           is_correct=is_correct,
                           current=index + 1, total=session.get("total", 0),
                           score=session.get("score", 0))


@app.route("/results")
def results():
    score = session.get("score", 0)
    total = session.get("total", 0)
    filename = session.get("filename", "")
    wrong_answers = session.get("wrong_answers", [])

    end_quiz(score, total)

    pct = int((score / total) * 100) if total > 0 else 0
    if pct >= 90:
        grade = ("Excellent", "green")
    elif pct >= 70:
        grade = ("Good", "blue")
    elif pct >= 50:
        grade = ("Pass", "orange")
    else:
        grade = ("Try Again", "red")

    wrong_mgr = WrongAnswerManager()
    for q in wrong_answers:
        wrong_mgr.add_wrong_answer(q)

    return render_template("results.html", score=score, total=total,
                           pct=pct, grade=grade, filename=filename)


# ── WSGI entry point for GoDaddy ─────────────────────────────────────────────

application = app

if __name__ == "__main__":
    app.run(debug=True, port=8081)
