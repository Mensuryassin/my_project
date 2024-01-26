from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.video import Video


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')  
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.valid_user(request.form):
        
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['Password'])
    }
    id = User.save(data)
    session['user_id'] = id
   
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login(): 
    user = User.get_by_email(request.form)
    if not User:
        flash("invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['Password']):
        flash("invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': session['user_id']
    }
    return render_template("dashboard.html", videos=Video.get_all(data) ,user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()                               
    return redirect('/ ')       