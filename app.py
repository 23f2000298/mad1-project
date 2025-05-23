from flask import Flask,request,render_template,redirect,url_for
from models import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#initializing object in the flask application context..

db.init_app(app)
bcript.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
            return 'User registered successfully'
        else:
            return 'User already exists'
        
    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug = True)
