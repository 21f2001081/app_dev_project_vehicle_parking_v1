from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from applications.models import *
from datetime import datetime
from sqlalchemy import func, extract

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
            return redirect(url_for('user_dashboard'))
    
        elif admin and admin.password == password:
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
        
@app.route('/home')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
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

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    return render_template('admin/admin_dashboard.html')

@app.route('/admin/users')
def manage_users():
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/search', methods=['GET', 'POST'])
def admin_search():
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    
    search_result = None
    search_type = None

    if request.method == 'POST':
        search_by = request.form.get('search_by')
        search_value = request.form.get('search_value')

        if search_by == 'user_id':
            search_type = 'user'
            if search_value.isdigit():
                search_result = User.query.filter_by(id=int(search_value)).first()
        elif search_by == 'location':
            search_type = 'lot'
            search_result = Parking_lot.query.filter(Parking_lot.location.ilike(f"%{search_value}%")).all()

    return render_template('admin/search.html', search_type=search_type, result=search_result)

@app.route('/admin/lots')
def manage_lots():
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))

    lots = Parking_lot.query.all()
    return render_template('admin/manage_lots.html', lots=lots)


@app.route('/admin/lots/new', methods=['GET', 'POST'])
def add_lot():
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form['location']
        address = request.form['address']
        pincode = request.form['pincode']
        price = request.form['price']
        max_no_spots = int(request.form['max_no_spots'])
        landmark = request.form['landmark']

        new_lot = Parking_lot(
            location=location,
            address=address,
            pincode=pincode,
            price=price,
            max_no_spots=max_no_spots,
            landmark=landmark
        )
        db.session.add(new_lot)
        db.session.commit()

        # Auto-create spots
        for _ in range(max_no_spots):
            spot = Parking_spot(parking_lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        return redirect(url_for('manage_lots'))

    return render_template('admin/add_lot.html')

@app.route('/admin/lots/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))

    lot = Parking_lot.query.get_or_404(lot_id)

    if request.method == 'POST':
        lot.location = request.form['location']
        lot.address = request.form['address']
        lot.pincode = request.form['pincode']
        lot.price = request.form['price']
        lot.landmark = request.form['landmark']
        db.session.commit()
        return redirect(url_for('manage_lots'))

    return render_template('admin/edit_lot.html', lot=lot)

@app.route('/admin/lots/view/<int:lot_id>')
def view_lot(lot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))

    lot = Parking_lot.query.get_or_404(lot_id)
    spots = Parking_spot.query.filter_by(parking_lot_id=lot_id).all()
    return render_template('admin/view_lot.html', lot=lot, spots=spots)

@app.route('/admin/lots/delete/<int:lot_id>')
def delete_lot(lot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))

    lot = Parking_lot.query.get_or_404(lot_id)

    # Check if any spot in this lot is occupied
    occupied_spot = any(spot.is_booked for spot in lot.parking_spots)
    if occupied_spot:
        flash("Cannot delete the parking lot. Some spots are still occupied.", "danger")
        return redirect(url_for('manage_lots'))

    # Safe to delete
    db.session.delete(lot)
    db.session.commit()
    flash("Parking lot deleted successfully.", "success")
    return redirect(url_for('manage_lots'))


@app.route('/admin/spot/<int:spot_id>')
def view_spot(spot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    
    spot = Parking_spot.query.get_or_404(spot_id)
    return render_template('admin/view_spot.html', spot=spot)

# # Route to delete a parking spot (if available)
# @app.route('/admin/spot/delete/<int:spot_id>', methods=['POST'])
# def delete_spot(spot_id):
#     if 'admin_id' not in session:
#         flash('You need to log in as an admin first.', 'error')
#         return redirect(url_for('login'))
#     spot = Parking_spot.query.get_or_404(spot_id)
#     if spot.is_booked:
#         flash("Cannot delete an occupied spot.", "danger")
#     else:
#         db.session.delete(spot)
#         db.session.commit()
#         flash("Spot deleted successfully.", "success")
#     return redirect(url_for('view_lot', lot_id=spot.parking_lot_id))

@app.route('/admin/spot/unavailable/<int:spot_id>', methods=['POST'])
def mark_spot_unavailable(spot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    
    spot = Parking_spot.query.get_or_404(spot_id)
    if not spot.is_booked:
        spot.additional_info = 'Unavailable'
        db.session.commit()
        flash("Spot marked as unavailable.", "success")
    else:
        flash("Cannot mark an occupied spot as unavailable.", "danger")
    
    return redirect(url_for('view_spot', spot_id=spot.id))


# Route to view booking for a given spot
@app.route('/admin/spot/<int:spot_id>/booking')
def spot_booking(spot_id):
    if 'admin_id' not in session:
        flash('You need to log in as an admin first.', 'error')
        return redirect(url_for('login'))
    spot = Parking_spot.query.get_or_404(spot_id)
    booking = Booking.query.filter_by(parking_spot_id=spot.id).order_by(Booking.start_time.desc()).first()
    if not booking:
        flash("No booking found for this spot.", "warning")
        return redirect(url_for('view_spot', spot_id=spot.id))
    user = User.query.get(booking.user_id)
    return render_template('admin/spot_booking.html', booking=booking, user=user, spot=spot)

@app.route('/admin/bookings')
def view_all_bookings():
    if 'admin_id' not in session:
        flash('Please login as admin.', 'danger')
        return redirect(url_for('login'))

    bookings = Booking.query.order_by(Booking.start_time.desc()).all()
    return render_template('admin/all_bookings.html', bookings=bookings)

@app.route('/admin/summary')
def admin_summary():
    # Revenue from each lot
    revenue_data = db.session.query(
        Parking_lot.location,
        func.sum(Booking.cost).label('total_revenue')
    ).join(Parking_spot, Parking_spot.parking_lot_id == Parking_lot.id).join(Booking, Booking.parking_spot_id == Parking_spot.id).group_by(Parking_lot.id).all()

    # Occupancy per lot (available vs occupied)
    occupancy_data = db.session.query(
        Parking_lot.location,
        func.count(func.nullif(Parking_spot.is_booked, False)).label('occupied'),
        func.count(func.nullif(Parking_spot.is_booked, True)).label('available')
    ).join(Parking_spot).group_by(Parking_lot.id).all()

    return render_template('admin/summary.html', revenue_data=revenue_data, occupancy_data=occupancy_data)

@app.route('/admin/profile')
def admin_profile():
    if 'admin_id' not in session:
        flash('Please log in as admin.', 'warning')
        return redirect(url_for('login'))
    admin = Admin.query.get(session['admin_id'])
    return render_template('admin/profile.html', admin=admin)

@app.route('/admin/profile/edit', methods=['GET', 'POST'])
def edit_admin_profile():
    if 'admin_id' not in session:
        flash('Please log in as admin.', 'warning')
        return redirect(url_for('login'))

    admin = Admin.query.get(session['admin_id'])

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username:
            admin.username = username
        if password:
            admin.password = password

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_profile'))

    return render_template('admin/edit_profile.html', admin=admin)
    

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.start_time.desc()).all()
    return render_template('user/dashboard.html', user=user, bookings=bookings)

@app.route('/user/search', methods=['POST'])
def search_parking():
    search_type = request.form['search_type']
    query = request.form['query']
    if search_type == 'location':
        lots = Parking_lot.query.filter(Parking_lot.location.ilike(f"%{query}%")).all()
    elif search_type == 'pincode':
        lots = Parking_lot.query.filter_by(pincode=query).all()
    else:
        lots = []
    return render_template('user/search_results.html', lots=lots)

@app.route('/user/book/<int:lot_id>')
def reserve_spot(lot_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    lot = Parking_lot.query.get_or_404(lot_id)
    spot = Parking_spot.query.filter_by(parking_lot_id=lot_id, is_booked=False).filter(
        (Parking_spot.additional_info != 'Unavailable') | (Parking_spot.additional_info.is_(None))
    ).first()
    if not spot:
        flash('No available spots.', 'danger')
        return redirect(url_for('user_dashboard'))
    return render_template('user/reserve_form.html', lot=lot, spot=spot, user_id=session['user_id'])

@app.route('/user/book/confirm', methods=['POST'])
def confirm_reservation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    lot_id = int(request.form['lot_id'])
    spot_id = int(request.form['spot_id'])
    vehicle_number = request.form['vehicle_number']
    now = datetime.now()
    booking = Booking(
        user_id=user_id,
        parking_spot_id=spot_id,
        start_time=now,
        end_time=now,
        cost=0,
        vehicle_number=vehicle_number
    )
    spot = Parking_spot.query.get_or_404(spot_id)
    spot.is_booked = True
    db.session.add(booking)
    db.session.commit()
    flash('Reservation successful.', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user/release/<int:booking_id>')
def release_form(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    booking = Booking.query.get_or_404(booking_id)
    now = datetime.now()
    return render_template('user/release_form.html', booking=booking, now=now)

@app.route('/user/release/confirm', methods=['POST'])
def confirm_release():
    booking_id = int(request.form['booking_id'])
    booking = Booking.query.get_or_404(booking_id)
    now = datetime.now()
    booking.end_time = now
    # Calculate duration and cost
    duration = (booking.end_time - booking.start_time).total_seconds() / 60  # in minutes
    rate = booking.parking_spot.parking_lot.price
    booking.cost = int(rate * (duration / 60))  # hourly rate
    booking.parking_spot.is_booked = False
    db.session.commit()
    flash('Spot released.', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user/profile')
def user_profile():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(session['user_id'])
    return render_template('user/profile.html', user=user)

@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_user_profile():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.address = request.form['address']
        user.pincode = request.form['pincode']
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('user_profile'))

    return render_template('user/edit_profile.html', user=user)

@app.route('/user/summary')
def user_summary():
    if 'user_id' not in session:
        flash('Please log in to view summary.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Total cost
    total_cost = db.session.query(func.sum(Booking.cost))\
        .filter_by(user_id=user_id).scalar() or 0

    # Cost per month
    monthly_data = db.session.query(
        extract('month', Booking.start_time).label('month'),
        func.sum(Booking.cost).label('total')
    ).filter_by(user_id=user_id)\
     .group_by('month')\
     .order_by('month')\
     .all()

    months = [datetime(2024, int(row.month), 1).strftime('%B') for row in monthly_data]
    monthly_costs = [row.total for row in monthly_data]

    # Cost per parking lot
    lot_data = (
    db.session.query(
        Parking_lot.location,
        func.sum(Booking.cost)
    )
    .join(Parking_spot, Booking.parking_spot_id == Parking_spot.id)
    .join(Parking_lot, Parking_spot.parking_lot_id == Parking_lot.id)
    .filter(Booking.user_id == user_id)
    .group_by(Parking_lot.location)
    .all())

    lot_names = [row[0] for row in lot_data]
    lot_costs = [row[1] for row in lot_data]

    return render_template(
        'user/summary.html',
        total_cost=total_cost,
        months=months,
        monthly_costs=monthly_costs,
        lot_names=lot_names,
        lot_costs=lot_costs
    )
