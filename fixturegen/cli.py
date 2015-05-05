import click

from fixturegen.exc import NoSuchTable, WrongDSN
from fixturegen.generator import generate, sqlalchemy_data

@click.command()
@click.argument('dsn', required=True)
@click.argument('table', required=True)
@click.option('--limit', help='Limit fixture count', type=click.INT)
@click.option('--where', help='Filter result. i.e. "id > 2"')
@click.option('--order-by', help='Order fixture output. i.e. "id DESC"')
def sqlalchemy(dsn, table, limit=None, where=None, order_by=None):
    """
    Provide DSN and Table name for fixture generation
    """
    try:
        click.echo(generate(*sqlalchemy_data(table, dsn, limit, where, order_by)))
    except NoSuchTable:
        click.echo('No such table', err=True)
    except WrongDSN:
        click.echo('Wrong DSN', err=True)
