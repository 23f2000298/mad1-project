from flask import Flask
from application.database import db #step3

import secrets #new
app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = secrets.token_hex(16)  #new
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3" 
    db.init_app(app)  #step3
    app.app_context().push()
    return app
app = create_app()
from application.contollers import * #step2

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username = "admin123").first():
            user1 = User(username = "admin123",email = "admin@123",password ="1",type = "admin")
            db.session.add(user1)
            db.session.commit()
    app.run(debug = True)