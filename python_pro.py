#encoding:utf-8
from flask import Flask, render_template, url_for,request,redirect, session,flash,abort
from flask_login import login_required,current_user
from flask_mail import Mail,Message
import config
from models import User,Post,Comment
from exts import db
from flask_moment import Moment, datetime
from flask_login import LoginManager
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import os
github_blueprint = make_github_blueprint(client_id='c2c15a15be9fd57d1a4d',client_secret='ae65d378f2173d8085a6cea0f3f15a19ad480ebe')
google_blueprint = make_google_blueprint(client_id= '922468949333-u5t6edqk3e2ftjqe2o08eqi1miik53u8.apps.googleusercontent.com', client_secret='W1aMQ6AmdDnp5ZI4P-JWPQ5F')
twitter_blueprint = make_twitter_blueprint(api_key='bUs6VVgAqpp8KfvldZUu7Hyc4', api_secret= 'lpTocRhuNPYw8gsQos5tT4OBXLxaROPw5CoJVQK8TylMxU7hpV')
login_manager=LoginManager()
app = Flask(__name__)
app.config.from_object(config)
# followings are email configurations
os.environ['MAIL_USERNAME']= 'jimmy.zgp'
os.environ['MAIL_PASSPORD']='50425968'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']='587'
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSPORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASK]'
app.config['FLASK_MAIL_SENDER']='Flasky Admin <jimmy.zgp@gmail.com>'
#initilize databasw with the instance of app
db.init_app(app)
mail=Mail(app)
login_manager.init_app(app)
moment = Moment(app)
login_manager.login_view='login'
app.register_blueprint(google_blueprint,url_prefix='/google_login')
app.register_blueprint(github_blueprint,url_prefix='/github')
app.register_blueprint(twitter_blueprint,url_prefix='/twitter_login')

#   sending confirmation email
def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=app.config['FLASK_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    mail.send(msg)

@app.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v2/userinfo")

        return render_template('index.html')

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()

        return '<h1>Your Twitter name is @{}'.format(account_info_json['screen_name'])

    return '<h1>Request failed!</h1>'

@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()

        return '<h1>Your Github name is {}'.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'

@app.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts = posts)

@app.route('/login/', methods= ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email, User.password == password).first()

        if user:
            session['user_id'] = user.id
            # login not required within 31 days
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return 'you have input incorrect username or password'

@app.route('/logout/')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
    # del session['user_id']
        return redirect(url_for('login'))

@app.route('/register/', methods= ['GET','POST'])
def register():
    from models import User
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter(User.email == email).first()
        if user:
            return 'The email you entered has already been used'
        else:
            user = User(username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()

            #if successfully register, redirect to login page
            return redirect(url_for('login'))

@app.route('/question/',methods= ['GET','POST'])
@login_required
def question():
        if request.method == "POST":
            postname = request.form.get('title')
            body = request.form.get('content')
            author_id = session.get('user_id')
            timestamp = datetime.utcnow()
            post = Post(postname = postname, body=body, timestamp = timestamp,author_id=author_id)
            db.session.add(post)
            db.session.commit()
            posts = Post.query.order_by(Post.timestamp.desc()).all()
            return render_template('index.html', posts = posts)

        return render_template('question.html')

@app.route('/details/<post_id>')
@login_required
def details(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    post.comments.comment
    return render_template('details.html',post=post)

@app.route('/add_comment/', methods=['POST'])
def add_comment():
    commentInfo = request.form.get("comment")
    post_id = request.form.get('post_id')
    comment = Comment(comment=commentInfo)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user

    post = Post.query.filter(Post.id == post_id).first()
    comment.post=post
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('details',post_id=post_id))


@app.route('/profile/', methods=['GET','POST'])
@login_required
def profile():
    '''user = User.query.filter(username = username).first()
    if user is None:
        return "not logged in"'''


    return render_template('profile.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    else:
        return {}


if __name__ =='__main__':
    app.run()
