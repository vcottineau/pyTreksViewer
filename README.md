# pyTreksViewer
![pyTreksViewer.png](../master/docs/pyTreksViewer.png)

**pyTreksViwer** is a simple python web applications based on [Flask](https://pypi.org/project/Flask/), [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) and [alembic](https://pypi.org/project/alembic/). Routing services are provided by [openrouteservice](https://pypi.org/project/openrouteservice/) and gpx manipulations by [gpxpy](https://pypi.org/project/gpxpy/). Javascript librairies used in this project are [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/), [Leaflet](https://leafletjs.com/) and [Chart.js](https://www.chartjs.org/).

## Installing
- Install and update using [pipenv](https://pypi.org/project/pipenv/):

```
pipenv update --dev
```

- Add environment variables to .env file:

```
SECRET_KEY=d9ce2a7949f6485185a58dacae8e8490
ORS_TOKEN=492d994621b34f4fab436de2779782fc
```

- Init SQLite database:

```
flask db init
flask db migrate
flask db upgrade
```

- Run the following SQL scripts:
[profile.sql](../master/docs/scripts/profile.sql)
[preference.sql](../master/docs/scripts/preference.sql)
[country.sql](../master/docs/scripts/country.sql)
[folder.sql](../master/docs/scripts/folder.sql)

## Usage
- Run the appplication:

```flask run```


## Documentation
![SchemaSpy_ERD.png](../master/docs/SchemaSpy_ERD.png)

## License
**pyTrekViewer** is licensed under the MIT License.
