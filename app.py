from flask import Flask, render_template, request, flash, redirect, session
from models import db, connect_db
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback
from forms import CreateUserForm, LogInForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized



app = Flask(__name__)
# app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback' #Add database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['WTF_CSRF_ENABLED'] = False

# toolbar = DebugToolbarExtension(app)


with app.app_context():
    
    connect_db(app)
    #  this create tables every time the aplication runs
    db.create_all()  


############################### REGISTER #####$####################################   
  
@app.route('/')
def homepage():
    
    return redirect('/register')
        
    
@app.route('/register', methods=['GET','POST'])
def register():
    
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    
    form=CreateUserForm()
    
    if form.validate_on_submit():
       username = form.username.data
       password = form.password.data
       email = form.email.data
       first_name = form.first_name.data
       last_name=form.last_name.data
       
       user = User.register(username, password,email,first_name,last_name)
       db.session.commit()
       
       session['username']= user.username
       
       return redirect (f'/users/{user.username}')
    else:
        return render_template('user/register.html', form=form)
   
 
 ############################### Login and Logout #####$####################################   

 
   
@app.route('/login', methods=['GET','POST'])
def login():
    
    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    
    form = LogInForm()
    
    if form.validate_on_submit():
       username = form.username.data
       password = form.password.data 
       
       user = User.authenticate(username, password)
       if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
       else:
           form.username.errors=['Invalid username/password']
           return render_template('user/login.html', form=form)
    
    return render_template('user/login.html', form=form)

@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
   


 ############################### User  #####$####################################   

@app.route('/users/<username>', methods=['GET'])
def user_profile(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("user/profile.html", user=user, form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.clear()
    
    return redirect('/login')


 ############################### Feedback Routes #####$####################################   



@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    if user.username != username:
        raise Unauthorized()

    form=FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
    
        feedback = Feedback(title=title,content=content,username=username)
        db.session.add(feedback)
        db.session.commit()
         
        return redirect(f'/users/{feedback.username}')
    
    else:
        return render_template('feedback/create_feedback_form.html', form=form)
     
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)
    
    
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    if form.validate_on_submit():
        feedback.title =form.title.data,
        feedback.content = form.content.data   
        db.session.commit()
        
        return redirect(f'/users/{feedback.username}')
    
    return render_template('feedback/update_feedback_form.html', form=form, feedback=feedback)
    


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    
    feedback=Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
        
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        
    return redirect(f'/users/{feedback.username}')



if __name__ == '__main__':
    app.run(debug=True)