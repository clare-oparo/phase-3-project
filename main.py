import click
from init_db import init_db
from models.book import Book
from models.reading_goal import ReadingGoal
from models.review import Review
from models.note import Note 
import json
import random 
import csv 
import sys 

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
    post_action_prompt()


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
    
    post_action_prompt()
    

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
    
    post_action_prompt()

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

    post_action_prompt()

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
    post_action_prompt()


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
    click.echo(f'Review added for "{selected_book.name}".')

    post_action_prompt()


@click.command()
def suggest_next():
    #"""Generate reading suggestions"""
    try:
        with open('suggestions.json', 'r') as f:
            suggestions = json.load(f)
            book = random.choice(suggestions)
            click.echo(f'How about reading {book['name']} by {book['author']}?')
    except (FileNotFoundError, json.JSONDecodeError):
        click.echo('Unable to load book suggestions.')
    
    post_action_prompt()
                  


@click.command()
def export_list():
    #"""Exporting reading list to a csv file"""
    books = db_session.query(Book).all()
    filename = 'reading_list.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author', 'genre','total_pages','status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in books:
            writer.writerow({'title':book.name, 'author':book.author, 'genre':book.genre})

    click.echo(f'Your reading list has been exported to {filename}')

    post_action_prompt()

@click.group(name='book_notes')
def book_notes():
    """Manage book notes."""
    pass

@book_notes.command(name='add')
@click.option('--book_id', type=int, prompt='Book ID')
@click.option('--content', type=str, prompt='Note content')

def add_note(book_id, content):
    #'''Add a new note to a book.'''
    book = db_session.query(Book).filter_by(id=book_id).first()
    if book:
        new_note = Note(content=content, book=book)
        db_session.add(new_note)
        db_session.commit()
        click.echo(f'Note added to {book.name}')
    else:
        click.echo('Book not found.')
    
    post_action_prompt()

@book_notes.command(name='view')
@click.option('--book_id', type=int, prompt='Book ID')

def view_notes(book_id):
    '''View notes for a specific book.'''
    notes = db_session.query(Note).filter_by(book_id=book_id).all()
    if notes:
        click.echo(f'Notes for Book ID {book_id}: ')
        for note in notes:
            click.echo(f'ID: {note.id}, Content: {note.content}')
    
    else:
        click.echo('No notes found for this book.')
    
    post_action_prompt()
    
@book_notes.command(name='update')
@click.option('--note_id', type=int, prompt='Note ID')
@click.option('--content', type=str, prompt='New note content')
def update_note(note_id, content):
    '''Update a specific note'''
    note = db_session.query(Note).filter_by(id=note_id).first()
    if note:
        note.content = content
        db_session.commit()
        click.echo(f'Note ID: {note_id} updated.')
    else:
        click.echo('Note not found.')

    post_action_prompt()

@book_notes.command(name='delete')
@click.option('--note_id', type=int, prompt='Note ID')
def delete_note(note_id):
    '''Delete a specific note'''
    note = db_session.query(Note).filter_by(id=note_id).first()
    if note:
        db_session.delete(note)
        db_session.commit()
        click.echo(f'Note ID {note_id} deleted.')
    else:
        click.echo('Note not found')
    
    post_action_prompt()

#register commands
cli.add_command(add_book)
cli.add_command(view_books)
cli.add_command(update_status)
cli.add_command(set_goal)
cli.add_command(update_goal)
cli.add_command(add_review)
cli.add_command(suggest_next)
cli.add_command(export_list)
cli.add_command(book_notes)


def show_menu():
    #"""Display menu to user"""
    click.echo('Welcome to LibLog! Select...')
    click.echo('1 to Add a new book')
    click.echo('2 to View books and IDs')
    click.echo('3 to Update status')
    click.echo('4 to Set reading goal')
    click.echo('5 to Update reading goal')
    click.echo('6 to Rate and review a book')
    click.echo('7 for Book suggestions')
    click.echo('8 to Export reading list')
    click.echo('9 to Manage book notes')
    click.echo('10 to Quit')
    
    while True:
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
        elif choice == 9:
            book_notes()
        elif choice == 10:
            click.echo('Goodbye!')
            sys.exit()
        else:
            click.echo('Invalid choice. Please choose a valid option.')

def post_action_prompt():
    click.echo("\nWhat would you like to do next?")
    click.echo("1: Return to Main Menu")
    click.echo("2: Quit")
    choice = click.prompt("Please enter your choice", type=int)
    
    if choice == 1:
        show_menu()
    else:
        click.echo('Goodbye!')
        sys.exit()


if __name__ == '__main__':
    show_menu() 
    # cli()