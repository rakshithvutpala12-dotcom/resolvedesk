import click
from flask.cli import with_appcontext
from .extensions import db
from .models import User

@click.command('create-admin')
@with_appcontext
def create_admin():
    name = click.prompt('Administrator name')
    email = click.prompt('Administrator email').strip().lower()
    if User.query.filter_by(email=email).first():
        raise click.ClickException('An account with that email already exists.')
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    if len(password) < 8:
        raise click.ClickException('Password must be at least 8 characters.')
    user = User(name=name, email=email, role='admin', department='IT Support')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Administrator account created for {email}.')
