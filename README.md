# pyTreksViewer
![pyTreksViewer.png](../master/docs/pyTreksViewer.png)

**pyTreksViwer** is a simple python web applications based on [Flask](https://pypi.org/project/Flask/), [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) and [alembic](https://pypi.org/project/alembic/). Routing services are provided by [openrouteservice](https://pypi.org/project/openrouteservice/) and gpx manipulations by [gpxpy](https://pypi.org/project/gpxpy/). Javascript librairies used in this project are [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/), [Leaflet](https://leafletjs.com/) and [Chart.js](https://www.chartjs.org/).

## Installing
- Install and update using [pipenv](https://pypi.org/project/pipenv/):

```
pipenv update --dev
```

- Add environment variables to .env file and set values:

```
SECRET_KEY=YOUR_SECRET_KEY
ORS_TOKEN=YOUR_ORS_API_KEY
```

- Create SQLite database:

```
flask sqlite create
```

## Usage
- Run the appplication:

```
flask run
```

## Documentation
![SchemaSpy_ERD.png](../master/docs/SchemaSpy_ERD.png)

## License
**pyTrekViewer** is licensed under the MIT License.
