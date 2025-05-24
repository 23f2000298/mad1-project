from flask import Flask,request,render_template,redirect,url_for,flash
from models import *
from config import Config
from flask_login import LoginManager,login_user,login_required,logout_user,current_user

app = Flask(__name__)
app.config.from_object(Config)

#initializing object in the flask application context..

db.init_app(app)
bcript.init_app(app)

login_manager = LoginManager(app) #when we are using login manager  use must use secret key in config file
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#creating user
def create_admin():
    existing_admin = User.query.filter_by(admin = True).first()    
    if existing_admin:
        return
    new_admin = User(name='admin',email='admin@123',password=bcript.generate_password_hash('1').decode('utf-8'))
    new_admin.admin = True
    db.session.add(new_admin)
    db.session.commit()
    return "Admin created successfully"

with app.app_context():
    db.create_all()
    create_admin()

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

if __name__ == '__main__':
    app.run(debug = True)
