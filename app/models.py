from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy


from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'

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


class Trek(db.Model):
    __tablename__ = 'trek'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('preference.id'))    

    routes = db.relationship('Route',
        backref=db.backref('trek'),
        order_by='Route.position',
        collection_class=ordering_list('position'))
    
    def __init__(self, **kwargs):
        super(Trek, self).__init__(**kwargs)
        if self.profile is None:
            self.profile = Profile.query.filter_by(default=True).first()
        if self.preference is None:
            self.preference = Preference.query.filter_by(default=True).first()

    def __repr__(self):
        return '<Trek {}>'.format(self.name)


class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(8192))
    distance = db.Column(db.Float)
    ascent = db.Column(db.Float)
    descent = db.Column(db.Float)
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('preference.id'))    

    _markers = db.relationship('RouteMarker',
        order_by='RouteMarker.position',
        collection_class=ordering_list('position'))

    markers = association_proxy('_markers', 'marker',
        creator=lambda m: RouteMarker(marker=m))

    def __init__(self, **kwargs):
        super(Route, self).__init__(**kwargs)


class Marker(db.Model):
    __tablename__ = 'marker'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    address = db.Column(db.String(128), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Marker, self).__init__(**kwargs)

    def __repr__(self):
        return '<Marker {}>'.format(self.name)


class RouteMarker(db.Model):
    __tablename__ = 'route_marker'

    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), primary_key=True)
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    route = db.relationship('Route',
        backref=db.backref("trek_routes",
        cascade="all, delete-orphan"))

    marker = db.relationship("Marker")


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek', backref='profile', lazy='dynamic')
    routes = db.relationship('Route', backref='profile', lazy='dynamic')
    
    @staticmethod
    def insert_modes():
        modes = ['Driving', 'Cycling', 'Walking', 'Hicking']
        default_mode = 'Cycling'
        for m in modes:
            profile = Profile.query.filter_by(name=m).first()
            if profile is None:
                profile = Profile(name=m)
            profile.default = (profile.name == default_mode)
            db.session.add(profile)
        db.session.commit()
    
    def __repr__(self):
        return '<Profile {}>'.format(self.name)


class Preference(db.Model):
    __tablename__ = 'preference'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek', backref='preference', lazy='dynamic')
    routes = db.relationship('Route', backref='preference', lazy='dynamic')
    
    @staticmethod
    def insert_options():
        options = ['Fastest', 'Shortest', 'Recommended']
        default_option = 'Shortest'
        for o in options:
            preference = Preference.query.filter_by(name=o).first()
            if preference is None:
                preference = Preference(name=o)
            preference.default = (preference.name == default_option)
            db.session.add(preference)
        db.session.commit()

    def __repr__(self):
        return '<Preference {}>'.format(self.name)