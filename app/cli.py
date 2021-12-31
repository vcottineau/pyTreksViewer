import os
import click


from flask import current_app
from sqlalchemy import text


from app import db


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')

    @app.cli.group()
    def sqlite():
        """Run SQLite commands."""
        pass

    @sqlite.command()
    def create():
        """Create the initial database."""
        db.drop_all()
        db.create_all()

        scripts = [
            './docs/scripts/country.sql',
            './docs/scripts/folder.sql',
            './docs/scripts/preference.sql',
            './docs/scripts/profile.sql'
        ]
        
        for script in scripts:
            with open(script) as f:
                script_file = f.read()
                for statement in script_file.split(';'):
                    db.session.execute(statement)
                    
    @app.cli.group()
    def test():
        """Unit testing framework commands."""
        pass

    @test.command()
    def run():
        """Run unit testing framework."""
        if os.system('coverage run -m unittest discover'):
            raise RuntimeError('')

    @test.command()
    def report():
        """Report unit testing framework."""
        if os.system('coverage report -m'):
            raise RuntimeError('')

    @app.cli.group()
    def doc():
        """Build documentation."""
        pass

    @doc.command()
    def generate():
        "Generate entity relationship diagram."
        if os.system('./schemaspy/schemaspy'):
            raise RuntimeError('')
