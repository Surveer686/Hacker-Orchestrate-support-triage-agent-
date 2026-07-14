from __future__ import annotations

import os

from flask import Flask, render_template, request

from agent import AgentConfig, SupportTriageAgent

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(repo_root, "data")

app = Flask(
    __name__,
    template_folder=os.path.join(repo_root, "templates"),
    static_folder=os.path.join(repo_root, "static"),
)

agent = SupportTriageAgent(AgentConfig(data_dir=data_dir))


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        issue = request.form.get("issue", "").strip()
        company = request.form.get("company", "").strip()

        if not subject and not issue:
            error = "Please enter a ticket subject or issue description."
        else:
            result = agent.process_ticket(subject=subject, issue=issue, company=company)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
