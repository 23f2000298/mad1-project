from flask import Flask,request,redirect,url_for,render_template,flash
from models import *
from functools import wraps
from config import Config
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from werkzeug.utils import secure_filename,os


app = Flask(__name__)
app.config.from_object(Config)

#initializing object in the flask application context..

db.init_app(app)
bcript.init_app(app)

login_manager = LoginManager(app) #when we are using login manager  use must use secret key in config file
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))

#creating user
def create_admin():
    existing_admin = User.query.filter_by(admin = True).first()    
    if existing_admin:
        return
    new_admin = User(name='admin',email='admin@123',password="1")
    new_admin.admin = True
    db.session.add(new_admin)
    db.session.commit()
    return "Admin created successfully"

with app.app_context():
    db.create_all()
    create_admin()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            flash("You must be Admin to access this page","error")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #retrieve form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        #check if use already exists
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            #creating new user
            user = User(name=name,email=email,password=password)
        #adding the use to the database
            db.session.add(user)
            db.session.commit()
            flash ('User registered successfully',"success")
            return redirect(url_for('login'))
        else:
            flash ('User already exists')
        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #retrive from the data
        email = request.form['email']
        password = request.form['password']
        #user querring
        user = User.query.filter_by(email=email).first()
        #if email and passwor match
        if user and Bcrypt().check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

############# crud 0n parking lot ################

@app.route('/Parking_Lot/create',methods=['GET','POST'])    
@login_required
@admin_required
def create_parking_lot():
    if request.method == 'POST':
        location = request.form['location']
        capacity = request.form['capacity']
        price = request.form['price']
        new_parking_lot = ParkingLot(location=location,capacity=capacity,price=price)
        db.session.add(new_parking_lot)
        db.session.commit()
        flash("Parking lot created successfully","success")
        return redirect(url_for('list_parking_lots'))
    return render_template('parking_lots/create.html')

@app.route('/parking_lots')
@login_required
def list_parking_lots():
    parking_lots = ParkingLot.query.all()
    return render_template('parking_lots/list.html',parking_lots=parking_lots)

@app.route('/parking_lots/<int:parking_lot_id>/edit',methods=['GET','PUT'])
@login_required
@admin_required
def edit_parking_lot(parking_lot_id):
    parking_lot = ParkingLot.query.get_or_404(parking_lot_id)
    if request.method == 'PUT':
        parking_lot.name = request.form['name']
        parking_lot.address = request.form['address']
        db.session.commit()
        flash("Parking lot updated successfully","success")
        return redirect(url_for('list_parking_lots'))
    return render_template('parking_lots/edit.html',parking_lot=parking_lot)

@app.route('/parking_lots/<int:parking_lot_id>/delete',methods=['POST'])
@login_required
@admin_required
def delete_parking_lot(parking_lot_id):    
    parking_lot = ParkingLot.query.get_or_404(parking_lot_id)
    db.session.delete(parking_lot)
    db.session.commit()
    flash("Parking lot deleted successfully","success")
    return redirect(url_for('list_parking_lots'))
      

if __name__ == '__main__':
    app.run(debug = True)
