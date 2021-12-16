from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'ILSAM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #
db.init_app(app) 

def create_app():

   
    
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login
    
    from models import User
    @login_manager.user_loader
    def load_user(user_id): 
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
   
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app