from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.video import Video
from flask_app.models.user import User





@app.route('/new/video')
def new_video():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("new_video.html", user=User.get_by_id(data))

@app.route('/create/video', methods=['POST']) 
def create_video():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Video.valid_video(request.form):
        return redirect ('/new/video')
    data = {
        "title": request.form["title"],
        "genre" : request.form["genre"],
        "description" : request.form["description"],
        "date_made" : request.form["date_made"],
        "user_id": session["user_id"]
    }
    Video.save(data)
    return redirect('/dashboard')

@app.route('/edit/video/<int:id>')
def edit_video(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = { 
        "id":session['user_id']
    }
    return render_template("edit_video.html", videos=Video.get_one(data) ,user = User.get_by_id(user_data))

@app.route('/update/video/<int:id>', methods =['POST'])
def update_video(id):
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if  not Video.valid_video(request.form):
        return redirect(f'/edit/video/{id}')   
    data = {
        "title": request.form["title"],
        "genre": request.form["genre"],
        "description": request.form["description"],
        "date_made": request.form["date_made"],
        "id" : id 
    return redirect('/dashboard')

@app.route('/view/video/<int:id>')
def show_video(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']  
    }
    return render_template("show_video.html", videos=Video.get_one(data), user=User.get_by_id(user_data))

@app.route('/video')
def video():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("video.html", user=User.get_by_id(data))

@app.route('/destroy/video/<int:id>')
def destroy_video(id):  
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Video.destroy(data)
    return redirect('/dashboard')