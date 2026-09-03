from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = "ore2-development-secret-key"

# Simple in-memory defaults. For a real deployment, replace this with SQLite.
DEFAULT_TASKS = [
    {"id": 1, "title": "Programming Fundamentals", "course": "CCP6114", "hours": 6, "priority": "High", "done": False},
    {"id": 2, "title": "Cybersecurity reading", "course": "Cybersecurity", "hours": 4, "priority": "Medium", "done": False},
    {"id": 3, "title": "Database assignment", "course": "Database Systems", "hours": 5, "priority": "High", "done": True},
    {"id": 4, "title": "Group project meeting", "course": "Software Engineering", "hours": 2, "priority": "Low", "done": False},
]

def get_tasks():
    if "tasks" not in session:
        session["tasks"] = DEFAULT_TASKS
    return session["tasks"]

def save_tasks(tasks):
    session["tasks"] = tasks
    session.modified = True

def workload_data(tasks):
    total = sum(t["hours"] for t in tasks)
    mental = min(100, round(sum(t["hours"] for t in tasks if t["priority"] == "High") / max(total, 1) * 100 + 20))
    time_load = min(100, round(total / 20 * 100))
    physical = 65
    social = 55
    overall = min(100, round((mental + time_load + physical + social) / 4))
    return {
        "overall": overall,
        "mental": mental,
        "time": time_load,
        "physical": physical,
        "social": social,
        "total_hours": total
    }

@app.route("/")
def home():
    return render_template("home.html", active="home")

@app.route("/workload")
def workload():
    tasks = get_tasks()
    return render_template("workload.html", active="workload", data=workload_data(tasks))

@app.route("/breakdown")
def breakdown():
    tasks = get_tasks()
    data = workload_data(tasks)
    cards = [
        {
            "name": "Mental",
            "score": data["mental"],
            "color_class": "coral",
            "contributors": ["Programming / coding", "Upcoming deadlines", "Poor sleep quality"]
        },
        {
            "name": "Time",
            "score": data["time"],
            "color_class": "purple",
            "contributors": ["Part-time job hours", "Daily commute"]
        },
        {
            "name": "Physical",
            "score": data["physical"],
            "color_class": "navy",
            "contributors": ["Gym or sport 3 days", "Poor sleep quality"]
        },
        {
            "name": "Social",
            "score": data["social"],
            "color_class": "red",
            "contributors": ["2 group projects", "Family check-in call"]
        },
        {
            "name": "Errands",
            "score": 82,
            "color_class": "orange",
            "contributors": ["Groceries, laundry, bills"]
        }
    ]
    return render_template("breakdown.html", active="breakdown", data=data, cards=cards)

@app.route("/planner", methods=["GET", "POST"])
def planner():
    tasks = get_tasks()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        course = request.form.get("course", "").strip()
        hours = request.form.get("hours", "1")
        priority = request.form.get("priority", "Medium")

        if title:
            try:
                hours = max(1, min(40, int(hours)))
            except ValueError:
                hours = 1

            new_id = max([t["id"] for t in tasks], default=0) + 1
            tasks.append({
                "id": new_id,
                "title": title,
                "course": course or "General",
                "hours": hours,
                "priority": priority,
                "done": False
            })
            save_tasks(tasks)

        return redirect(url_for("planner"))

    return render_template(
        "planner.html",
        active="planner",
        tasks=tasks,
        data=workload_data(tasks)
    )

@app.post("/planner/toggle/<int:task_id>")
def toggle_task(task_id):
    tasks = get_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    save_tasks(tasks)
    return redirect(url_for("planner"))

@app.post("/planner/delete/<int:task_id>")
def delete_task(task_id):
    tasks = [t for t in get_tasks() if t["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("planner"))

@app.post("/self-test")
def self_test():
    # A tiny server-side self-test endpoint used by the button in the header.
    tasks = get_tasks()
    score = workload_data(tasks)["overall"]
    if score >= 80:
        message = "Your workload is high. Consider dropping one non-essential task."
    elif score >= 60:
        message = "Your workload is elevated. Schedule a recovery block this week."
    else:
        message = "Your workload looks manageable. Keep your buffer for unexpected work."
    return jsonify({"score": score, "message": message})

@app.template_filter("datetime")
def format_datetime(value):
    return value.strftime("%d %b %Y")

if __name__ == "__main__":
    app.run(debug=True)
