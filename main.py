from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:myblogzfinal@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '12qwaszx34erdfcv'
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id') )

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users) 

@app.route('/blog', methods = ['POST', 'GET'])   
def list_blogs():
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    posts = Blog.query.all()

    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', entries=entries)
        
    if blog_id == None: 
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog_page.html', user_id=blog_id, posts=posts, title='Blog Home Page')
   
    if blog_id == "":
        posts = Blog.query.all()
        return render_template('add_blog.html')

    else:
        if (blog_id):
            post = Blog.query.filter_by(id=blog_id).first()
            return render_template('entry.html', post=post, title=post.title, body=post.body, user=post.owner.username, user_id=post.owner_id)
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['entry']
        new_entry = Blog(blog_title, blog_body, owner)
        title_err = ''
        body_err = ''
        
        if not blog_title or not blog_body:
            title_err = "Please fill in a title"
            body_err = "Please fill in blog body"
            return render_template('add_blog.html', blog_title=blog_title, title_err=title_err, body_err=body_err)
        if not body_err and not title_err:
            db.session.add(new_entry)
            db.session.commit() 
            return redirect('/blog?id={}'.format(new_entry.id)) 
           
    blogs = Blog.query.filter_by(owner=owner).all()
    return render_template('add_blog.html', blogs=blogs)

@app.route('/entry', methods=['POST', 'GET'])
def entry():
       
    return render_template('entry.html')

def has_char(chex):
    if chex != "":
        return True
    else:
        return False

def space(verify):
    whitespace = " "
    if whitespace not in verify:
        return True
    else:
        return False


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        error = ""
        pass_err = ""
        verify_err = ""

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username, password)
            if len(username) < 3:
                error = "Invalid Username. Please enter a username with at least 3 characters"
                username = ""

            if len(password) < 3:
                pass_err = "Invalid Password. Please enter a password with at least 3 characters"
            if password != verify:
                verify_err ="Please enter a matching password"
            if not error and not pass_err and not verify_err:
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                return render_template('signup.html', username=username, error=error, pass_err=pass_err, verify_err=verify_err)    
        else:
          
            return "<h1>Duplicate user</h1>"
     
       
    return render_template('signup.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/singleUser', methods=['GET'])
def singleUser():
    users = User.query.filter_by(username=session['user_id']).first()
    user_id = request.args.get('users')
    blogs = Blog.query.filter_by(username=user_id).all()
    return render_template('singleUser.html', users=users, blogs=blogs)


if  __name__ == "__main__":
    app.run()

