from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'todos' not in session:
        session['todos'] = []
    return render_template('index.html', todos=session['todos'])

@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')
    if 'todos' not in session:
        session['todos'] = []
    todo_id = str(uuid.uuid4())  # Generate a unique ID for the new to-do item
    session['todos'].append({"id": todo_id, "task": todo, "date": datetime.now().strftime("%Y-%m-%d"), "completed": False})
    session.modified = True
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>')
def delete_todo(todo_id):
    print(todo_id)
    print(session['todos'][0]['id'])
    session['todos'] = [todo for todo in session['todos'] if todo['id'] != todo_id]
    session.modified = True
    return redirect(url_for('index'))

@app.route('/complete/<todo_id>')
def complete_todo(todo_id):
    for todo in session['todos']:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    session.modified = True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
