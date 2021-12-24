from app import create_app, db
from app.models import Trek, Marker


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Trek': Trek, 'Marker': Marker}

if __name__ == '__main__':
    app.run()