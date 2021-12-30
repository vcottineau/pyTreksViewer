from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired


from app.models import Marker, Profile, Preference, Country, Folder


class TrekForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "Name"}, validators=[DataRequired()])
    submit = SubmitField('Submit')


class TrekRouteForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "Name"}, validators=[DataRequired()])
    profile = SelectField('Profile', coerce=int)
    preference = SelectField('Preference', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TrekRouteForm, self).__init__(*args, **kwargs)
        self.profile.choices = [(profile.id, profile.name) for profile in Profile.query.all()]
        self.preference.choices = [(preference.id, preference.name) for preference in Preference.query.all()]


class TrekRouteMarkerForm(FlaskForm):
    marker = SelectField('Marker', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TrekRouteMarkerForm, self).__init__(*args, **kwargs)
        self.marker.choices = [(marker.id, marker.name) for marker in Marker.query.order_by(Marker.name).all()]


class MarkerForm(FlaskForm):
    folder = SelectField('Folder', coerce=int)
    name = StringField('Name', render_kw={"placeholder": "Name"}, validators=[DataRequired()])
    mode = SelectField('Mode', coerce=int)
    country = SelectField('Country', coerce=int)
    address = StringField('Address', render_kw={"placeholder": "Address"}, validators=[DataRequired()])    
    latitude = FloatField('Latitude', render_kw={"placeholder": "Latitude", "disabled": True})
    longitude = FloatField('Longitude', render_kw={"placeholder": "Longitude", "disabled": True})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(MarkerForm, self).__init__(*args, **kwargs)
        self.folder.choices = [(folder.id, folder.name) for folder in Folder.query.order_by(Folder.name).all()]
        self.country.choices = [(country.id, country.name) for country in Country.query.order_by(Country.name).all()]
        self.mode.choices = [(1, "Address"), (2, "Coordinates")]
