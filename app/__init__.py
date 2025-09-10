from flask import Flask
#from app.extensions import ma
from .extensions import ma
from .models import db
from .blueprints.mechanics import mechanics_bp
from .blueprints.serviceTicket import serviceTickets_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(serviceTickets_bp, url_prefix='/serviceTickets')

    return app