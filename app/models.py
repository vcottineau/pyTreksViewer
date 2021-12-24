from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from flask_login import UserMixin


from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class TrekMarker(db.Model):
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('mode.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    markers = db.relationship('TrekMarker',
        foreign_keys=[TrekMarker.trek_id],
        backref=db.backref('trek', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Trek, self).__init__(**kwargs)
        if self.mode is None:
            self.mode = Mode.query.filter_by(default=True).first()
        if self.option is None:
            self.option = Option.query.filter_by(default=True).first()

    def add_marker(self, marker):
        trek_marker = TrekMarker(trek=self, marker=marker)
        db.session.add(trek_marker)

    def remove_marker(self, marker):
        trek_marker = self.markers.filter_by(marker_id=marker.id).first()
        db.session.delete(trek_marker)

    def __repr__(self):
        return '<Trek {}>'.format(self.name)


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(8192))

    start_id = db.Column(db.Integer, db.ForeignKey('marker.id'))
    end_id = db.Column(db.Integer, db.ForeignKey('marker.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('mode.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Route, self).__init__(**kwargs)


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    address = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('TrekMarker',
        foreign_keys=[TrekMarker.marker_id],
        backref=db.backref('marker', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')

    start_markers = db.relationship('Route',
                                    foreign_keys='Route.start_id',
                                    backref='start_marker', lazy='dynamic')

    end_markers = db.relationship('Route',
                                  foreign_keys='Route.end_id',
                                  backref='end_marker', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Marker, self).__init__(**kwargs)

    def __repr__(self):
        return '<Marker {}>'.format(self.name)


class Mode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek', backref='mode', lazy='dynamic')
    routes = db.relationship('Route', backref='mode', lazy='dynamic')
    
    @staticmethod
    def insert_modes():
        modes = ['Driving', 'Cycling', 'Hicking']
        default_mode = 'Cycling'
        for m in modes:
            mode = Mode.query.filter_by(name=m).first()
            if mode is None:
                mode = Mode(name=m)
            mode.default = (mode.name == default_mode)
            db.session.add(mode)
        db.session.commit()
    
    def __repr__(self):
        return '<Mode {}>'.format(self.name)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek', backref='option', lazy='dynamic')
    routes = db.relationship('Route', backref='option', lazy='dynamic')
    
    @staticmethod
    def insert_options():
        options = ['Fastest', 'Shortest']
        default_option = 'Shortest'
        for o in options:
            option = Option.query.filter_by(name=o).first()
            if option is None:
                option = Option(name=o)
            option.default = (option.name == default_option)
            db.session.add(option)
        db.session.commit()

    def __repr__(self):
        return '<Option {}>'.format(self.name)