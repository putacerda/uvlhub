import os
import importlib
import click
from flask.cli import with_appcontext

from app.seeders.BaseSeeder import BaseSeeder
from rosemary.commands.db_reset import db_reset


def get_module_seeders(module_path, specific_module=None):
    seeders = []
    for root, dirs, files in os.walk(module_path):
        if 'seeder.py' in files:
            relative_path = os.path.relpath(root, module_path)
            module_name = relative_path.replace(os.path.sep, '.')
            full_module_name = f'app.blueprints.{module_name}.seeder'

            # Si se especificó un módulo y no coincide con el actual, continúa con el siguiente
            if specific_module and specific_module != module_name.split('.')[0]:
                continue

            seeder_module = importlib.import_module(full_module_name)
            importlib.reload(seeder_module)  # Recargar el módulo

            for attr in dir(seeder_module):
                if attr.endswith('Seeder'):
                    seeder_class = getattr(seeder_module, attr)
                    if issubclass(seeder_class, BaseSeeder) and seeder_class is not BaseSeeder:
                        seeders.append(seeder_class())
    return seeders


@click.command('db:seed', help="Populates the database with the seeders defined in each module.")
@click.option('--reset', is_flag=True, help="Reset the database before seeding.")
@click.argument('module', required=False)
@with_appcontext
def db_seed(reset, module):

    if reset:
        if click.confirm(click.style('This will reset the database, do you want to continue?', fg='red'), abort=True):
            click.echo(click.style("Resetting the database...", fg='yellow'))
            ctx = click.get_current_context()
            ctx.invoke(db_reset, clear_migrations=False, yes=True)
            click.echo(click.style("Database reset successfully.", fg='green'))
        else:
            click.echo(click.style("Database reset cancelled.", fg='yellow'))
            return

    blueprints_module_path = '/app/app/blueprints'
    seeders = get_module_seeders(blueprints_module_path, specific_module=module)
    success = True  # Flag to control the successful flow of the operation

    if module:
        click.echo(click.style(f"Seeding data for the '{module}' module...", fg='green'))
    else:
        click.echo(click.style("Seeding data for all modules...", fg='green'))

    for seeder in seeders:
        try:
            seeder.run()
            click.echo(click.style(f'{seeder.__class__.__name__} performed.', fg='blue'))
        except Exception as e:
            click.echo(click.style(f'Error running seeder {seeder.__class__.__name__}: {e}', fg='red'))
            click.echo(click.style(f'Rolled back the transaction of {seeder.__class__.__name__} to keep the session '
                                   f'clean.',
                                   fg='yellow'))

            success = False
            break

    if success:
        click.echo(click.style('Database populated with test data.', fg='green'))