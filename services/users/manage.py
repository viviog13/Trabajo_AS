import unittest

from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import User  # <-- nuevo

app = create_app()  # <-- nuevo
cli = FlaskGroup(create_app=create_app)  # <-- nuevo

# nuevo
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
	    return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(titulo='Mil caeran', autor='Susi', añodepublicacion='1990', editorial='Ni idea', generoliterario='Accion'))
    db.session.add(User(titulo='La casa verde', autor='Mario', añodepublicacion='1966', editorial='Six Barral', generoliterario='Ficcion'))
    db.session.commit()

if __name__ == "__main__":
	cli()