from flask import Flask, render_template, request, redirect, url_for
import json
import os
import subprocess
import glob
import yaml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def timeline(): 
    scenarios = glob.glob("scenarios/*.yml")
    scenarios = [os.path.basename(s) for s in scenarios]

    if request.method == 'POST':
        selected = request.form.get('scenario')
        if selected:
            scenario_path = os.path.join("scenarios", selected)
            subprocess.run(["python3", "main.py", "--scenario", scenario_path])
            return redirect(url_for('timeline'))

    # Load run log
    if os.path.exists("outputs/run_log.json"):
        with open("outputs/run_log.json", "r") as f:
            steps = json.load(f)
    else:
        steps = []

    return render_template("timeline.html", steps=steps, scenarios=scenarios)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            steps = json.loads(request.form['scenario_json'])
            filename = request.form.get('filename', 'new_scenario.yml')
            path = os.path.join("scenarios", filename)

            with open(path, 'w') as f:
                yaml.dump(steps, f, default_flow_style=False)

            return redirect(url_for('timeline'))
        except Exception as e:
            return f"Error saving scenario: {e}", 400

    return render_template("create.html")

if __name__ == '__main__':
    app.run(debug=True)
