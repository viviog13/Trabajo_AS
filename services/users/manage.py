import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import User  # <-- nuevo

# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

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

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == "__main__":
	cli()