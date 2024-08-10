import os

from markupsafe import escape
from flask import Flask, abort, render_template, request, url_for, flash, redirect
import datetime 
from forms import CourseForm
import sqlite3


app = Flask(__name__)

# LESSON 1 basic routing

# @app.route('/')
# @app.route('/index/')
# def hello():
#     return '<h1>Hello World</h1>'

# @app.route('/about/')
# def about():
#     return '<h3>This is a Flask application</h3>'

# @app.route('/capitalize/<word>/')
# def capitalize(word):
#     return '<h1>{}</h1>'.format(escape(word.capitalize()))

# @app.route('/add/<int:n1>/<int:n2>/')
# def add(n1,n2):
#     return '<h1>{}</h1>'.format(n1+n2)

# @app.route('/users/<int:user_id>/')
# def greet_user(user_id):
#     users = ['bob', 'adam', 'alice']
#     try:
#         return '<h3>Hi {}</h3>'.format(users[user_id])
#     except IndexError:
#         abort(404)


# Lesson 2 templating with jinja

@app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.now(datetime.UTC))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.',
                ]
    
    return render_template('comments.html', comments=comments)

# LESSON 3 Error handling

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# @app.route('/messages/<int:idx>/')
# def message(idx):
#     app.logger.info("Building the message list...")
#     messages = ['Message Zero', 'Message One', 'Message Two']
#     try:
#         app.logger.debug("Get message with index: {}".format(idx))
#         return render_template('messages.html', message=messages[idx])
#     except IndexError:
#         app.logger.error("Index {} is causing an IndexError".format(idx))
#         abort(404)


# LESSON 4 FORMS_1 - use of web forms

app.config['SECRET_KEY'] = "mysecretkey"
messages = [
    {
    "title": "Message One",
    "content": "Message One Content"
    },
    {
    "title": "Message Two",
    "content": "Message Two Content"
    },
    {
    "title": "Message Three",
    "content": "Message Three Content"
    },
]
@app.route("/messages/")
def message():
    return render_template('message.html', messages=messages)

@app.route("/messages/create", methods=("GET","POST"))
def create_message():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('message'))
        
    return render_template("create_message.html")

# LESSON 5 FORMS_2 validate forms using Flask-WTF

courses_list = [
    {
        'title': 'Python 101',
        'description': 'Learn Python basics',
        'price': 34,
        'available': True,
        'level': 'Beginner',
    }
]

@app.route('/course')
def courses():
    return render_template('courses.html', courses=courses_list)

@app.route('/course/add', methods=['GET','POST'])
def course_add():
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({
            'title': form.title.data,
            'description': form.description.data,
            'price': form.price.data,
            'available': form.available.data,
            'level': form.level.data,
        })
        return redirect(url_for('courses'))
    return render_template('course_add.html', form=form)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/dbcourse')
def dbcourse():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('dbcourse.html', posts=posts)

@app.route('/dbcourse/create', methods=("GET", "POST"))
def dbcourse_create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('dbcourse'))
    return render_template('dbcourse_create.html')



if __name__ == "__main__":
    app.run(debug=True)