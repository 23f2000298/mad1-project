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

@app.route('/parking_lots/create',methods=['GET','POST'])    
@login_required
@admin_required
def create_parking_lot():
    if request.method == 'POST':
      
        name = request.form['name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        price_per_hour = request.form['price_per_hour']
        maximum_spots = request.form['maximum_spots']
        new_parking_lot = ParkingLot(name=name,address=address,pin_code=pin_code,price_per_hour=price_per_hour,maximum_spots=maximum_spots)
        db.session.add(new_parking_lot)
        db.session.commit()
        flash("Parking lot created successfully","success")
        return redirect(url_for('list_parking_lots'))
    return render_template('parking_lots/create.html')

@app.route('/parking_lots')
@login_required
def list_parking_lots():
    query = request.args.get('search',"")
    if query:
        parking_lots = ParkingLot.query.filter(ParkingLot.name.ilike(f"%{query}%")).all()
    else:
        parking_lots = ParkingLot.query.all()
    return render_template('parking_lots/list.html',parking_lots=parking_lots)

@app.route('/parking_lots/<int:parking_lot_id>/edit',methods=['GET','POST'])
@login_required
@admin_required
def edit_parking_lot(parking_lot_id):
    parking_lot = ParkingLot.query.get_or_404(parking_lot_id)
    if request.method == 'POST':
        parking_lot.name = request.form['name']
        parking_lot.address = request.form['address']
        parking_lot.pin_code = request.form['pin_code']
        parking_lot.price_per_hour = request.form['price_per_hour']
        parking_lot.maximum_spots = request.form['maximum_spots']
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
      
#######################crud on parking spots#####################
@app.route("/parking_spots/create",methods=['GET','POST'])
@login_required
@admin_required
def create_parking_spot():
    parking_lots = ParkingLot.query.all()
    if request.method == 'POST':
        #display from data
        # name = request.form['name']
        parking_lot_id = request.form['parking_lot_id']
        vehicle_no = request.form["vehical_no"]
        parking_spot_no = request.form["parking_spot_no"]
        estimate_parking_cost = request.form["estimate_parking_cost"]
        date = request.form["date"]
       
        pdf_file = request.files.get("pdf_file")
        pdf_path = None

        if pdf_file and pdf_file.filename != "":
            filename = secure_filename(name)
            pdf_path = filename
            os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"]),exist_ok = True)
            pdf_file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))

        parking_spot = ParkingSpot(vehicle_no = vehicle_no,
                                   date = date,estimate_parking_cost = estimate_parking_cost,
                                   parking_lot_id = parking_lot_id,
                                   parking_spot_no = parking_spot_no,)
        db.session.add(parking_spot)
        db.session.commit()
        flash("Parking spot created successfully","success")
        return redirect(url_for('list_parking_spots',parking_lots = parking_lots))    
    
    return render_template('parking_spots/create.html')

@app.route('/parking_spots')
@login_required
def list_parking_spots():   
    query = request.args.get('search',"")
    # name = request.args.get('name',"")
    vehicle_no = request.args.get('vehicle_no',"")
    parking_lot_id = request.args.get('parking_lot_id',"")
    parking_spots_query = ParkingSpot.query
    if query:
        parking_spots_query = parking_spots_query.filter(ParkingSpot.name.ilike(f"%{query}%"))
    if vehicle_no:
        parking_spots_query = parking_spots_query.filter(ParkingSpot.vehical_no.ilike(f"%{vehicle_no}%"))
    if parking_lot_id:
         parking_spots_query = parking_spots_query.filter(ParkingSpot.parking_lot_id.ilike(f"%{parking_lot_id}%"))
    
    parking_spots = parking_spots_query.all()
    parking_lots = ParkingLot.query.all()
    # vehical_no = request.args.get('vehical_no',"")
    return render_template('parking_spots/list.html',parking_spots = parking_spots,query = query,vehical_no = vehicle_no,parking_lot_id = parking_lot_id,parking_lots=parking_lots)
@app.route('/parking_spots/<int:parking_spot_id>/edit',methods=['GET','POST'])
@login_required
@admin_required
def edit_parking_spot(parking_spot_id):
    parking_spot = ParkingLot.query.get_or_404(parking_spot_id)
    parking_lots = ParkingLot.query.all()
    if request.method == 'POST':
        # parking_spot.name = request.form['name']
        parking_spot.vehicle_no = request.form['vehicle_no']
        parking_spot.parking_lot_id = request.form['parking_lot_id']
        parking_spot.parking_spot_no = request.form['parking_spot_no']
        parking_spot.estimate_parking_cost = request.form['estimate_parking_cost']
        parking_spot.date = request.form['date']
        db.session.commit()
        flash("Parking spot updated successfully","success")
        return redirect(url_for('list_parking_spots'))
    return render_template('parking_spots/edit.html',parking_spot=parking_spot,parking_lots=parking_lots)   

@app.route('/parking_spots/<int:parking_spot_id>/delete',methods=['POST'])
@login_required
@admin_required
def delete_parking_spot(parking_spot_id):    
    parking_spot = ParkingSpot.query.get_or_404(parking_spot_id)
    db.session.delete(parking_spot)
    db.session.commit()
    flash("Parking spot deleted successfully","success")
    return redirect(url_for('list_parking_spots'))

if __name__ == '__main__':
    app.run(debug = True)
