from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = '12qwaszx34erdfcv'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, name,):    #took out ownner
        self.name = name
        self.completed = False
        #self.owner = owner
'''

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    #body = db.Column(db.String(340))
    #tasks = db.relationship('Task', backref='owner')

    def __init__(self, name):
        self.name = name
        #self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            
            session['email'] = email
            flash("Logged in")
           
            return redirect('/')
        else:
            flash('User password incorrect or user does not exist', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET']) 
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validateuser's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            
            return redirect('/')
        else:
            # TODO - user better respons messaging
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')
'''

@app.route('/', methods=['POST', 'GET'])
def index():
    #owner = User.query.filter_by(email=session['email']).first()
    
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)# removed owner
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()
    #tasks = Task.query.filter_by(completed=False).all() #removed owner
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('blog_page.html', title=" Build a Blog", tasks=tasks) #removed completed_tasks=completed_tasks
@app.route('/add_blog', methods=['POST', 'GET'])
def new_blog():
    
    
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)# removed owner
        db.session.add(new_task) 
        db.session.commit()
    tasks = Task.query.all()
    
    return render_template('add_blog.html', title=" Add a Blog")



@app.route('/blog_page', methods=['POST'])
def blogs():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':

    app.run()