import math
import requests


import openrouteservice
from openrouteservice.convert import decode_polyline
from openrouteservice.geocode import pelias_search
from openrouteservice.elevation import elevation_point
from openrouteservice.directions import directions
import gpxpy
import gpxpy.gpx

from config import Config


ors_profile = {
    "Driving": "driving-car",       # "driving-hgv"
    "Cycling": "cycling-regular",   # "cycling-road", "cycling-mountain", "cycling-electric"
    "Walking": "foot-walking",
    "Hicking": "foot-hiking",
}


ors_preference = {
    "Fastest": "fastest",
    "Shortest": "shortest",
    "Recommended": "recommended",
}


ors_format = {
    "Geojson": "geojson",
    "Json": "json",
    "Gpx": "gpx",
}


class ORSClient:
    def __init__(self):
        self.client = openrouteservice.Client(Config.ORS_TOKEN)

    def search(self, address):
        try:
            request = pelias_search(
                client=self.client, text=address)
        except requests.exceptions.ConnectionError:
            return None

        geometry = request["features"][0]["geometry"]
        if len(geometry):
            return geometry["coordinates"]
        else:
            return None

    def elevation(self, latitude, longitude):
        coordinates = (longitude, latitude)
        try:
            request = elevation_point(
                client=self.client, geometry=coordinates,
                format_in="point", format_out=ors_format["Geojson"])
        except requests.exceptions.ConnectionError:
            return None

        geometry = request["geometry"]
        if len(geometry):
            return geometry["coordinates"][2]
        else:
            return None

    def directions(self, locations, profile, preference):
        coordinates = [(location.longitude, location.latitude) for location in locations]
        try:
            request = directions(client=self.client, coordinates=coordinates,
                                 profile=profile, preference=preference,
                                 elevation=True, instructions=False,
                                 format=ors_format["Json"])
        except requests.exceptions.ConnectionError:
            return None

        routes = request["routes"]
        if len(routes):
            properties = routes[0]["summary"]
            geometry = routes[0]["geometry"]
            return geometry, properties["distance"], properties["ascent"], properties["descent"]
        else:
            return None

    def decode_geometry(self, geometry):
        return decode_polyline(polyline=geometry, is3d=True)["coordinates"]

    def haversine(self, coord1, coord2):
        r = 6372800
        lat1, lon1 = (coord1[0], coord1[1])
        lat2, lon2 = (coord2[0], coord2[1])

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

        return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


ors_client = ORSClient()


def export_trek_as_gpx(trek):
    gpx = gpxpy.gpx.GPX()

    gpx.author_name = trek.user.username
    gpx.author_email = trek.user.email
    gpx.name = trek.name

    for route in trek.routes:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = route.name
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for location in route.coordinates():
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=location[0], longitude=location[1], elevation=location[2]))

        for marker in route.markers:
            gpx_waypoint = gpxpy.gpx.GPXWaypoint(name=marker.name, latitude=marker.latitude, longitude=marker.longitude, elevation=marker.elevation)
            gpx.waypoints.append(gpx_waypoint)

    return gpx.to_xml()
