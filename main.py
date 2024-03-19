import click
from init_db import init_db

db_session= init_db() #initialize DB session

@click.group()
def cli():
    """LibLog: Organize your reading."""
    pass

# define cli commands here
@click.command()
def add_book():
    """Add a new book"""
    # implementation
    click.echo("Add a new book...")

@click.command()
def view_books():
    """View your books"""
    # implementation
    click.echo('View your books...')

@click.command()
def update_status():
    """Update reading status"""
    #implementation
    click.echo('Update reading status...')

@click.command()
def log_progress():
    """Logging reading progress"""
    #implementation
    click.echo('Log your reading progress...')

@click.command()
def set_goal():
    """Set reading goal"""
    #implementation
    click.echo('Set reading goal...')

@click.command()
def update_goal():
    """Update reading goal"""
    #implementation
    click.echo('Update reading goal...')

@click.command()
def add_review():
    """Add reviews and ratings"""
    #implementation
    click.echo('Add reviews and ratings...')

@click.command()
def suggest_next():
    """Generate reading suggestions"""
    #implementation
    click.echo('You may like:{suggestions}') #figure out how to get {suggestions}

@click.command()
def export_list():
    """Exporting reading list"""
    #implementation
    click.echo('Share your reading list...')

#register commands
cli.add_command(add_book)
cli.add_command(view_books)
cli.add_command(update_status)
cli.add_command(log_progress)
cli.add_command(set_goal)
cli.add_command(update_goal)
cli.add_command(add_review)
cli.add_command(suggest_next)
cli.add_command(export_list)


def show_menu():
    """Display menu to user"""
    click.echo('Welcome to LibLog!')
    click.echo('Select 1 to Add a new book')
    click.echo('Select 2 to View your books')
    click.echo('Select 3 to Log your reading progress')
    click.echo('Select 4 to Set your reading goal')
    click.echo('Select 5 to Update your reading goal')
    click.echo('Select 6 to Rate and Review a book')
    click.echo('Select 7 to For reading suggestions')
    click.echo('Select 8 to Export your reading list')
    
    choice = click.prompt('Please enter your choice', type=int)

    if choice == 1:
        add_book()
    elif choice == 2:
        view_books()
    elif choice == 3:
        log_progress()
    elif choice == 4:
        set_goal()
    elif choice == 5:
        update_goal()
    elif choice == 6:
        add_review()
    elif choice == 7:
        suggest_next()
    elif choice == 8:
        export_list()
    
    else:
        click.echo('Invalid choice. Please choose a valid option.')



if __name__ == '__main__':
    cli()