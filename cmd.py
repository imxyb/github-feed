import click
import db

from app import app


@click.group()
def cmd():
    pass


@cmd.command()
def test_data():
    db.init()
    db.create_test_data()


@cmd.command()
def start_app():
    db.init()
    app.run()


if __name__ == '__main__':
    cmd()
