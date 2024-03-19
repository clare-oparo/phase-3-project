import click
from init_db import init_db

db_session= init_db() #initialize DB session

@click.group()
def cli():
    "***LibLog: Organize your reading.***"
    pass

# define cli commands here
if __name__ == '__main__':
    cli()