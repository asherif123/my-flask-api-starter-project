from .extensions import db, bcrypt
import datetime as dt
from marshmallow import Schema, fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.LargeBinary(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, password=None, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.email!r})>"

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def email_already_registered(self):
        result = User.query.filter_by(email=self.email).first()
        if result:
            return True
        return False


class UserSchema(Schema):
    """
    To serialize the user model to/from User(object) to/from JSON
    AND 
    Validate input data to user model
    """
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    # Write-only
    password = fields.Str(load_only=True, required=True)
    # Read-only
    created_at = fields.DateTime(dump_only=True)
    last_seen = fields.DateTime(dump_only=True)
    active = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
