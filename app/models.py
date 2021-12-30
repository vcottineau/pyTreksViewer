from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy


from app import db, login_manager
from app.geocoding import ors_client, ors_profile, ors_preference, export_trek_as_gpx


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    treks = db.relationship('Trek',
        backref='user',
        cascade="all, delete-orphan",
        order_by='Trek.position',
        collection_class=ordering_list('position'))

    markers = db.relationship('Marker',
        backref='user',
        cascade="all, delete-orphan",
        order_by='Marker.name',       
        lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, Email {self.email}, Treks {self.treks.count()}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Trek(db.Model):
    __tablename__ = 'trek'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    routes = db.relationship('Route',
        backref='trek',
        cascade="all, delete-orphan",
        order_by='Route.position',
        collection_class=ordering_list('position'))

    def __init__(self, **kwargs):
        super(Trek, self).__init__(**kwargs)

    def distance(self):
        return sum(route.distance for route in self.routes if route.distance is not None)

    def ascent(self):
        return sum(route.ascent for route in self.routes if route.ascent is not None)

    def descent(self):
        return sum(route.descent for route in self.routes if route.descent is not None)

    def nb_routes(self):
        return len(self.routes)

    def nb_markers(self):
        return sum(len(route.markers) for route in self.routes)

    def elevation_profile(self):
        coordinates = []
        for route in self.routes:
            coordinates.extend(route.coordinates())

        d = 0
        p = []
        p.append({"x": d, "y": coordinates[0][2]})
        
        for i in range(1, len(coordinates)):
            d += ors_client.haversine(
                [coordinates[i-1][0], coordinates[i-1][1]],
                [coordinates[i][0], coordinates[i][1]])
            p.append({"x": d/1000, "y": coordinates[i][2]})

        return p


    def gpx(self):
        return export_trek_as_gpx(self)

    def __repr__(self):
        return f"<Trek {self.name}, Routes {len(self.routes)}>"


class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(8192))
    distance = db.Column(db.Float)
    ascent = db.Column(db.Float)
    descent = db.Column(db.Float)
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'))
    mode_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('preference.id'))

    route_markers = db.relationship('RouteMarker',
        order_by='RouteMarker.position',
        backref='route',
        cascade='all, delete-orphan',
        collection_class=ordering_list('position'))

    markers = association_proxy('route_markers', 'marker',
        creator=lambda m: RouteMarker(marker=m))

    def __init__(self, **kwargs):
        super(Route, self).__init__(**kwargs)
        if self.profile is None:
            self.profile = Profile.query.filter_by(default=True).first()
        if self.preference is None:
            self.preference = Preference.query.filter_by(default=True).first()

    def coordinates(self):
        return [[marker[1], marker[0], marker[2]] for marker in ors_client.decode_geometry(self.path)]

    def update(self):
        self.path, self.distance, self.ascent, self.descent = ors_client.directions(
            self.markers, ors_profile[self.profile.name], ors_preference[self.preference.name])

    def nb_markers(self):
        return len(self.markers)

    def __repr__(self):
        return f"<Name {self.name}, Markers {len(self.markers)}>"


class Marker(db.Model):
    __tablename__ = 'marker'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    address = db.Column(db.String(128), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))

    route_markers = db.relationship('RouteMarker',
        cascade="all, delete-orphan",
        backref='marker')

    def update(self):
        self.longitude, self.latitude = ors_client.search(self.address + ", " + self.country.name)
        self.elevation = ors_client.elevation(self.latitude, self.longitude)

    def __repr__(self):
        return f"<Marker {self.name}, Latitude {self.latitude}, Longitude {self.longitude}, Elevation {self.elevation}>"


class RouteMarker(db.Model):
    __tablename__ = 'route_marker'

    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), primary_key=True)
    position = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    markers = db.relationship('Marker', backref='country', lazy='dynamic')

    def __repr__(self):
        return f"<Country {self.name}>"


class Folder(db.Model):
    __tablename__ = 'folder'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    markers = db.relationship('Marker', backref='folder', order_by=('Marker.name'), lazy='dynamic')

    def __repr__(self):
        return f"<Folder {self.name}>"


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
        return f"<Profile {self.name}, Default {self.default}>"


class Preference(db.Model):
    __tablename__ = 'preference'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
        return f"<Preference {self.name}, Default {self.default}>"
