from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    #completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        #self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

   # if request.method == 'POST':
        #task_name = request.form['task']
        #new_task = Task(task_name)
        #db.session.add(new_task)
        #db.session.commit()

    #tasks = Task.query.filter_by(completed=False).all()
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('blog_page.html', title="Build a Blog")


@app.route('/add_blog', methods=['POST'])
def addblog ():

    #task_id = int(request.form['task-id'])
    #task = Task.query.get(task_id)
    #task.completed = True
    db.session.add(task)
    db.session.commit()

    return render_template('add_blog.html')


if __name__ == '__main__':
    app.run()