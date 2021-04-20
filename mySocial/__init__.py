import configparser
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    Config = configparser.ConfigParser()
    Config.read("mySocial/config.ini")

    app = Flask(__name__)
    app.secret_key = Config.get('App', 'secret_key')

    USER_NAME = Config.get('Database', 'USER_NAME')
    PASSWORD =  Config.get('Database', 'PASSWORD')
    IP = Config.get('Database', 'IP')
    DB_NAME = Config.get('Database', 'DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+USER_NAME+":"+PASSWORD+"@"+IP+"/"+DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.get('App', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.jinja_env.add_extension('jinja2.ext.do')


    db.init_app(app)

    ### use flask-login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth.Login')) 


    from .auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .messaging.messaging import messaging as messaging_blueprint
    app.register_blueprint(messaging_blueprint)
    
    from .profile.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)
    
    from .searching.searching import searching as searching_blueprint
    app.register_blueprint(searching_blueprint)

    socketio.init_app(app)

    return app
