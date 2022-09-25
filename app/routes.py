from flask import render_template, flash, redirect, url_for, request
from app import app,query_db,login_manager
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime
import os, flask_login
from app.func import check_if_username_exist,hash_password,check_password,safe_convert,convert_back,allowed_file
from werkzeug.utils import secure_filename

# this file contains all the different routes, and the logic for communicating with the database

#Login Management

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    if check_if_username_exist(user_id) is False:
        return
    user = User()
    user.id = user_id
    return user

# -----

# home page/login/registration
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if flask_login.current_user.is_authenticated: return redirect(url_for('stream', username=safe_convert(flask_login.current_user.id)))
    form = IndexForm()
    if form.login.is_submitted() and form.login.submit.data:
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(safe_convert(form.login.username.data)), one=True)
        if user == None:
            flash('Username and/or Password incorrect')
        elif check_password(form.login.password.data,user['password']):
            user = User()
            user.id = safe_convert(form.login.username.data)
            flask_login.login_user(user,remember = form.login.remember_me)
            return redirect(url_for('stream', username=safe_convert(form.login.username.data)))
        else:
            flash('Username and/or Password incorrect')

    elif form.register.is_submitted() and form.register.submit.data:
        username = safe_convert(form.register.username.data)
        if check_if_username_exist(username):
            flash('Username not available')
        else:
            query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES("{}", "{}", "{}", "{}");'.format(username,safe_convert(form.register.first_name.data),
            safe_convert(form.register.last_name.data), hash_password(form.register.password.data)))
            return redirect(url_for('index'))
    return render_template('index.html', title='Welcome', form=form)


# content stream page
@app.route('/stream/<username>', methods=['GET', 'POST'])
@flask_login.login_required
def stream(username):
    username = safe_convert(username)
    if not safe_convert(flask_login.current_user.id) == username: username = safe_convert(flask_login.current_user.id)
    form = PostForm()
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    if form.is_submitted():
        if form.image.data:
            if allowed_file(form.image.data.filename):
                path = os.path.join(app.config['UPLOAD_PATH'], secure_filename(form.image.data.filename))
                form.image.data.save(path)
            else:
                flash('File type is not supported!', 'error')
                return redirect(url_for('stream', username=username))

        query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES({}, "{}", "{}", \'{}\');'.format(user['id'], form.content.data, form.image.data.filename, datetime.now()))
        return redirect(url_for('stream', username=username))

    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id={0}) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id={0}) OR p.u_id={0} ORDER BY p.creation_time DESC;'.format(user['id']))
    return render_template('stream.html', title='Stream', username=username, form=form, posts=posts)

# comment page for a given post and user.
@app.route('/comments/<username>/<int:p_id>', methods=['GET', 'POST'])
@flask_login.login_required
def comments(username, p_id):
    username = safe_convert(username)
    if not safe_convert(flask_login.current_user.id) == username: username = safe_convert(flask_login.current_user.id)
    form = CommentsForm()
    if form.is_submitted():
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES({}, {}, "{}", \'{}\');'.format(p_id, user['id'], safe_convert(form.comment.data), datetime.now()))
        return redirect(url_for('comments', username=username, p_id=p_id))

    post = query_db('SELECT * FROM Posts WHERE id={};'.format(p_id), one=True)
    all_comments = query_db('SELECT DISTINCT creation_time, comment, username FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(p_id))
    converted_comments = []
    for i,x in enumerate(all_comments): #Not the best approach, but for now... it will do.
        converted_comments.append({'comment': convert_back(x['comment']), 'creation_time': x['creation_time'], 'username': x['username']})
    return render_template('comments.html', title='Comments', username=username, form=form, post=post, comments=converted_comments)

# page for seeing and adding friends
@app.route('/friends/<username>', methods=['GET', 'POST'])
@flask_login.login_required
def friends(username):
    username = safe_convert(username)
    if not safe_convert(flask_login.current_user.id) == username: username = safe_convert(flask_login.current_user.id)
    form = FriendsForm()
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    if form.is_submitted():
        friend = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.username.data), one=True)
        if friend is None:
            flash('User does not exist', 'error')
        else:
            query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(user['id'], friend['id']))

    all_friends = query_db('SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(user['id'], user['id']))
    return render_template('friends.html', title='Friends', username=username, friends=all_friends, form=form)

# see and edit detailed profile information of a user
@app.route('/profile/<username>', methods=['GET', 'POST'])
@flask_login.login_required
def profile(username):
    username = safe_convert(username)
    form = ProfileForm()
    if form.is_submitted():
        query_db('UPDATE Users SET education="{}", employment="{}", music="{}", movie="{}", nationality="{}", birthday=\'{}\' WHERE username="{}" ;'.format(
            safe_convert(form.education.data), safe_convert(form.employment.data), safe_convert(form.music.data), safe_convert(form.movie.data), safe_convert(form.nationality.data), safe_convert(form.birthday.data), username
        ))
        return redirect(url_for('profile', username=username))

    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    # TODO: Convert back to normal string
    return render_template('profile.html', title='profile', username=username, user=user, form=form)

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401