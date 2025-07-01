from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from applications.models import *
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        admin= Admin.query.filter(Admin.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
    
        elif admin and admin.password == password:
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
        
@app.route('/home')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
    elif 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        return render_template('home.html', admin=admin)
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    # session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/') #return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if len(username) < 3 or len(username) > 64:
            flash('Username must be between 3 and 64 characters.', 'error')
            return redirect(url_for('register'))
        if not username.isalnum():
            flash('Username must be alphanumeric.', 'error')
            return redirect(url_for('register'))
        passhash = request.form['passhash']
        full_name = request.form['full_name']
        address = request.form['address']
        pincode = request.form['pincode']
        if len(pincode) != 6 or not pincode.isdigit():
            flash('Pincode must be a 6-digit number.', 'error')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        
        new_user = User(username=username, full_name=full_name, address=address, pincode=pincode)
        new_user.set_password(passhash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


    
