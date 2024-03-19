import click
from init_db import init_db
from models.book import Book
from models.reading_goal import ReadingGoal
from models.review import Review

db_session= init_db() #initialize DB session

@click.group()
def cli():
    """LibLog: Organize your reading."""
    pass

# define cli commands here
@click.command()
def add_book():
    #"""Add a new book."""
    name = click.prompt('Enter the book name')
    author = click.prompt('Enter the author\'s name')
    genre = click.prompt('Enter book genre')
    total_pages = click.prompt('Enter the total number of pages', type=int)

    new_book = Book(name=name, author=author, genre=genre, total_pages=total_pages)
    db_session.add(new_book)
    db_session.commit()

    click.echo(f'{name} by {author} has been added to your library.')

@click.command()
def view_books():
    #"""View your books"""
    books = db_session.query(Book).all()
    if books:
        click.echo('Your Books:')
        for book in books:
            click.echo(f' ID: {book.id}, Title: {book.name}, Author: {book.author}')
    else:
        click.echo('Your library is empty.')
    

@click.command()
def update_status():
    # """Update reading status"""
    book_id = click.prompt('Enter the book ID', type=int)
    new_status = click.prompt('Enter the new status(unread, in progress or complete)')

    book = db_session.query(Book).filter_by(id=book_id).first()
    if book:
        book.status = new_status
        db_session.commit()
        click.echo(f'Updated {book.name} to {new_status}')
    else:
        click.echo('Book not found.')

@click.command()
def set_goal():
    #"""Set reading goal"""
    existing_goal = db_session.query(ReadingGoal).filter_by(status='active').first()
    if existing_goal:
        click.echo('You already have an active reading goal')
        if not click.confirm('Do you want to replace it?'):
            return
        
        existing_goal.status = 'completed'
        db_session.commit()

    goal = click.prompt('How many books do you aim to read?')
    start_date = click.prompt("Enter the start date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))
    end_date = click.prompt("Enter the end date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))

    new_goal = ReadingGoal(goal=goal, start_date=start_date.date(), end_date=end_date.date(), status='active')
    db_session.add(new_goal)
    db_session.commit()
    click.echo("Your new reading goal has been set.")

@click.command()
def update_goal():
    # """Update the current active reading goal."""
    goal = db_session.query(ReadingGoal).filter_by(status='active').first()
    if not goal:
        click.echo("No active reading goal found.")
        return

    goal.goal = click.prompt("How many books do you aim to read?", default=goal.goal, type=int)
    goal.start_date = click.prompt("Enter the start date (YYYY-MM-DD)", default=goal.start_date, type=click.DateTime(formats=["%Y-%m-%d"])).date()
    goal.end_date = click.prompt("Enter the end date (YYYY-MM-DD)", default=goal.end_date, type=click.DateTime(formats=["%Y-%m-%d"])).date()
    
    db_session.commit()
    click.echo("Your reading goal has been updated.")


@click.command()
def add_review():
    # """Add reviews and ratings"""
    book_name = click.prompt("Enter the book title")
    books = db_session.query(Book).filter(Book.name.ilike(f'%{book_name}%')).all()

    if not books:
        click.echo("No books found with that title.")
        return

    if len(books) == 1:
        selected_book = books[0]
    else:
        click.echo("Multiple books found:")
        for i, book in enumerate(books, 1):
            click.echo(f"{i}: {book.name} by {book.author}")
        book_index = click.prompt("Please enter the number of the book you want to review", type=int) - 1

        if book_index >= len(books) or book_index < 0:
            click.echo("Invalid selection.")
            return
        selected_book = books[book_index]

    rating = click.prompt("Enter your rating (1-5)", type=int)
    review_text = click.prompt("Enter your review", default="", show_default=False)

    new_review = Review(book_id=selected_book.id, rating=rating, review=review_text)
    db_session.add(new_review)
    db_session.commit()
    click.echo(f'Review added for "{selected_book.title}".')


@click.command()
def suggest_next():
    """Generate reading suggestions"""
    #implementation
    click.echo('You may like:{suggestions}') # figure out how to get {suggestions}

@click.command()
def export_list():
    """Exporting reading list"""
    #implementation
    click.echo('Share your reading list...')

#register commands
cli.add_command(add_book)
cli.add_command(view_books)
cli.add_command(update_status)
cli.add_command(set_goal)
cli.add_command(update_goal)
cli.add_command(add_review)
cli.add_command(suggest_next)
cli.add_command(export_list)


def show_menu():
    """Display menu to user"""
    click.echo('Welcome to LibLog! Select...')
    click.echo('1 to Add a new book')
    click.echo('2 to View books and book IDs')
    click.echo('3 to Update status')
    click.echo('4 to Set reading goal')
    click.echo('5 to Update reading goal')
    click.echo('6 to Rate and Review a book')
    click.echo('7 to For reading suggestions')
    click.echo('8 to Export your reading list')
    click.echo('9 to Quit')
    
    choice = click.prompt('Please enter your choice', type=int)

    if choice == 1:
        add_book()
    elif choice == 2:
        view_books()
    elif choice == 3:
        update_status()
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
    show_menu()
    # cli()