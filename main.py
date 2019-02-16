from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = '12qwaszx34erdfcv'
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')   
def blog():
    blog_id = request.args.get('id')

    
    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog_page.html', posts=posts, title='Build-a-blog')
    else:
        post = Blog.query.get(blog_id)
        return render_template('add_blog.html', post=post, title='Blog Entry')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['entry']
        title_err = ''
        body_err = ''
        
        if not blog_title or not blog_body:
            title_err = "Please fill in a title"
            #return render_template('add_blog.html', title_err=title_err)
        #if not blog_body:
            body_err = "Please fill in blog body"
            return render_template('add_blog.html', blog_title=blog_title, title_err=title_err, body_err=body_err)
        if not body_err and not title_err:
            new_entry = Blog(blog_title, blog_body)     
            db.session.add(new_entry)
            db.session.commit()        
            #return redirect('/blog?id={}'.format(new_entry.id)) 
            return redirect('/blog')

    return render_template('add_blog.html')
    #return render_template('blog_page.html', title='New Entry', title_err=title_err, body_err=body_err, blog_title=blog_title, blog_body=blog_body)
    
    
'''
    @app.route('/entry', methods=['POST', 'GET'])
    def entry():
        return render_template('entry.html')
'''
if  __name__ == "__main__":
    app.run()

