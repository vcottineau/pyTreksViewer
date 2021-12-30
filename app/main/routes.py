import json
from io import BytesIO


from flask import render_template, flash, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user


from app import db
from app.main import bp
from app.main.forms import TrekForm, TrekRouteForm, TrekRouteMarkerForm, MarkerForm
from app.models import User, Trek, Route, Marker, Profile, Preference, Country, Folder



# @app.template_filter()
# def commafy(value):
#     value = float(value)
#     return "${:,.2f}".format(value)


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Maps', user=current_user)


@bp.route('/treks', methods=['GET'])
@login_required
def treks():
    return render_template('treks.html', title='Treks', user=current_user)


@bp.route('/trek/add', methods=['GET', 'POST'])
@login_required
def add_trek():
    form = TrekForm()
    if form.validate_on_submit():
        name = form.name.data
        current_user.treks.append(Trek(name=name))
        db.session.commit()
        flash('Trek has been added.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('edit_trek.html', form=form, title="Add")


@bp.route('/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trek(trek_id):
    form = TrekForm()
    trek = Trek.query.filter_by(id=trek_id).one()
    if form.validate_on_submit():
        trek.name = form.name.data
        db.session.commit()
        flash('Trek has been updated.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    form.name.data = trek.name
    return render_template('edit_trek.html', form=form, title="Edit", trek_id=trek_id)


@bp.route('/trek/<int:trek_id>/delete', methods=['GET'])
@login_required
def delete_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id).one()
    db.session.delete(trek)
    db.session.commit()
    flash('Trek has been deleted.')
    return redirect(url_for('main.treks'))


@bp.route('/trek/<int:trek_id>/routes', methods=['GET'])
@login_required
def trek_routes(trek_id):
    trek = Trek.query.filter_by(id=trek_id).one()
    return render_template('trek_routes.html', title='Routes', trek=trek)


@bp.route('/trek/<int:trek_id>/route/add', methods=['GET', 'POST'])
@login_required
def add_trek_route(trek_id):
    form = TrekRouteForm()
    default_profile = Profile.query.filter_by(default=1).one()
    default_preference = Preference.query.filter_by(default=1).one()
    form.profile.data = default_profile.id
    form.profile.data = default_preference.id
    if form.validate_on_submit():
        name = form.name.data
        profile = Profile.query.get(form.profile.data)
        preference = Preference.query.get(form.preference.data)
        trek = Trek.query.filter_by(id=trek_id).one()
        trek.routes.append(Route(name=name, profile=profile, preference=preference))
        db.session.commit()
        flash('Route has been added.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('edit_trek_route.html', form=form, title="Add", trek_id=trek_id)


@bp.route('/trek/<int:trek_id>/route/<int:route_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trek_route(trek_id, route_id):
    form = TrekRouteForm()
    route = Route.query.filter_by(id=route_id).one()
    if form.validate_on_submit():
        route.name = form.name.data
        profile = Profile.query.get(form.profile.data)
        preference = Preference.query.get(form.preference.data)
        if route.profile.id != profile or route.preference.id != preference:
            route.profile = profile
            route.preference = preference
            route.update()
        db.session.commit()
        flash('Route has been updated.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    form.name.data = route.name
    form.profile.data = route.profile.id
    form.preference.data = route.preference.id
    return render_template('edit_trek_route.html', form=form, title="Edit", trek_id=trek_id, route_id=route_id)


@bp.route('/trek/<int:trek_id>/route/<int:route_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_trek_route(trek_id, route_id):
    route = Route.query.filter_by(id=route_id).one()
    db.session.delete(route)
    db.session.commit()
    flash('Route has been deleted.')
    return redirect(url_for('main.trek_routes', trek_id=trek_id))


@bp.route('/trek/<int:trek_id>/route/<int:route_id>/markers', methods=['GET'])
@login_required
def trek_route_markers(trek_id, route_id):
    trek = Trek.query.filter_by(id=trek_id).one()
    route = Route.query.filter_by(id=route_id).one()
    return render_template('trek_routes_markers.html', title='Markers', trek=trek, routes=[route])


@bp.route('/trek/<int:trek_id>/route/<int:route_id>/marker/add', methods=['GET', 'POST'])
@login_required
def add_trek_route_marker(trek_id, route_id):
    form = TrekRouteMarkerForm()
    if form.validate_on_submit():
        route = Route.query.filter_by(id=route_id).one()
        marker = Marker.query.get(form.marker.data)
        route.markers.append(marker)
        if len(route.markers) > 1:
            route.update()
        db.session.commit()
        flash('Marker has been added.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('edit_trek_route_marker.html', form=form, title="Add", trek_id=trek_id, route_id=route_id)


@bp.route('/trek/<int:trek_id>/route/<int:route_id>/marker/<int:marker_id>/delete/<show_all>', methods=['GET'])
@login_required
def delete_trek_route_marker(trek_id, route_id, marker_id, show_all):
    route = Route.query.filter_by(id=route_id).one()
    for marker in route.markers:
        if marker.id == marker_id:
            route.markers.remove(marker)
    db.session.commit()
    if len(route.markers) > 1:
        route.update()
    db.session.commit()
    flash('Marker has been deleted.')
    if show_all:
        return redirect(url_for('main.trek_markers', trek_id=trek_id))
    return redirect(url_for('main.trek_route_markers', trek_id=trek_id, route_id=route_id))


@bp.route('/trek/<int:trek_id>/markers', methods=['GET'])
@login_required
def trek_markers(trek_id):
    trek = Trek.query.filter_by(id=trek_id).one()
    return render_template('trek_markers.html', title='Markers', trek=trek)


@bp.route('/markers', methods=['GET'])
@login_required
def markers():
    folders = Folder.query.order_by(Folder.name).all()
    return render_template('markers.html', title='Markers', user=current_user, folders=folders)


@bp.route('/marker/add', methods=['GET', 'POST'])
@login_required
def add_marker():
    form = MarkerForm()
    default_country = Country.query.filter_by(default=1).one()
    form.country.data = default_country.id
    if form.validate_on_submit():
        name = form.name.data
        mode = form.mode.data
        address = form.address.data
        country = Country.query.get(form.country.data)
        folder = Folder.query.get(form.folder.data)
        # latitude = form.latitude.data
        # longitude = form.longitude.data
        marker = Marker(folder=folder, name=name, country=country, address=address)
        marker.update()
        current_user.markers.append(marker)
        db.session.commit()
        flash('Marker has been added.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('edit_marker.html', form=form, title="Add")


@bp.route('/marker/<int:marker_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_marker(marker_id):
    form = MarkerForm()
    marker = Marker.query.filter_by(id=marker_id).one()
    if form.validate_on_submit():        
        marker.name = form.name.data
        marker.address = form.address.data
        marker.country = Country.query.get(form.country.data)
        marker.folder = Folder.query.get(form.folder.data)
        marker.update()
        db.session.commit()
        flash('Marker has been updated.')
        return jsonify(status='ok')
    if form.errors:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)    
    form.name.data = marker.name
    form.address.data = marker.address
    form.country.data = marker.country
    form.latitude.data = marker.latitude
    form.longitude.data = marker.longitude
    form.country.data = marker.country.id
    form.folder.data = marker.folder.id
    return render_template('edit_marker.html', form=form, title="Edit", marker_id=marker_id)


@bp.route('/marker/<int:marker_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_marker(marker_id):
    marker = Marker.query.filter_by(id=marker_id).one()
    db.session.delete(marker)
    db.session.commit()
    flash('Marker has been deleted.')
    return redirect(url_for('main.markers'))

@bp.route('/get-file/<int:trek_id>', methods=['GET'])
def get_file(trek_id):
    trek = Trek.query.filter_by(id=trek_id).one()
    gpx_filename = trek.name + ".gpx"
    gpx_file = BytesIO()
    gpx_file.write(str(trek.gpx()).encode('utf-8'))
    gpx_file.seek(0)
    return send_file(gpx_file, mimetype="application/gpx+xml", attachment_filename=gpx_filename, as_attachment=True)
