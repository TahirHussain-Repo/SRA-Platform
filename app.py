from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_sections():
    """Fetch available section names from the SQLite database."""
    conn = sqlite3.connect('sections_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Section %'")
    sections = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sections

def get_questions(section):
    """Fetch questions for a given section from the SQLite database."""
    conn = sqlite3.connect('sections_database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM [{section}]"
    cursor.execute(query)
    questions = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    conn.close()
    return headers, questions

@app.route('/')
def index():
    """Homepage displaying available sections."""
    sections = get_sections()
    return render_template('index.html', sections=sections)

@app.route('/section/<section_name>', methods=['GET', 'POST'])
def section(section_name):
    """Page for a specific section to display questions and collect answers."""
    headers, questions = get_questions(section_name)
    if request.method == 'POST':
        # Collect answers from the form submission
        answers = {key: request.form.get(key) for key in request.form.keys()}
        return render_template('submitted.html', section=section_name, answers=answers)

    return render_template('section.html', section=section_name, headers=headers, questions=questions)

@app.route('/submitted')
def submitted():
    """Page to confirm answers submission."""
    return render_template('submitted.html')

if __name__ == '__main__':
    app.run(debug=True)

