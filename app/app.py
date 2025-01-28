from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_todo = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    notes = Note.query.filter_by(is_todo=False).order_by(Note.created_at.desc()).all()
    todos = Note.query.filter_by(is_todo=True).order_by(Note.created_at.desc()).all()
    return render_template('index.html', notes=notes, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    content = request.form.get('content')
    is_todo = request.form.get('is_todo') == 'true'
    
    note = Note(title=title, content=content, is_todo=is_todo)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    todo = Note.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
