import os
import click


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
    def test():
        pass

    @test.command()
    def run():
        if os.system('coverage run -m unittest discover'):
            raise RuntimeError('')

    @test.command()
    def report():
        if os.system('coverage report -m'):
            raise RuntimeError('')

    @app.cli.group()
    def doc():
        pass

    @doc.command()
    def generate():
        if os.system('./schemaspy/schemaspy'):
            raise RuntimeError('')
