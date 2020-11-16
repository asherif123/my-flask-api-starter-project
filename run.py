from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, bcrypt
from .models import User
from . import auth


def create_app(config):
    """
    Create application factory, as explained here: 
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(auth.routes.auth_bp)
    return None

def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": User}

    app.shell_context_processor(shell_context)


app = create_app(Config)