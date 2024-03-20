import click
from init_db import init_db
from models.book import Book
from models.reading_goal import ReadingGoal
from models.review import Review
# from models.note import Note 
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
    name = click.prompt('Enter the book name')
    author = click.prompt('Enter the author\'s name')
    genre = click.prompt('Enter book genre')
    total_pages = click.prompt('Enter the total number of pages', type=int)

    new_book = Book(name=name, author=author, genre=genre, total_pages=total_pages)
    db_session.add(new_book)
    db_session.commit()

    click.echo(f'{name} by {author} has been added to your library.')
    book_mgt_post_action_prompt()


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
    
    book_mgt_post_action_prompt()
    

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
    
    book_mgt_post_action_prompt()

@click.command()
def delete_books():
    book_id = click.prompt('Enter the Book ID', type=int)
    book = db_session.query(Book).filter_by(id = book_id).first()

    if book:
        db_session.delete(book)
        db_session.commit()
        click.echo(f'{book.name} by {book.author} deleted successfully.')
    else:
        
        click.echo('Book not found.')
    
    book_mgt_post_action_prompt()

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


@click.group()
def reading_goal_mgt():
    reading_goal_menu()

@click.command()
def set_goal():
    existing_goals = db_session.query(ReadingGoal).filter_by(status='active').all()
    if existing_goals:
        click.echo(f'You already have {len(existing_goals)} active reading goal(s).')
    
    if not existing_goals or click.confirm('Do you want to add another goal?'):
        goal_number = click.prompt('How many books do you plan to read?', type=int)
        start_date = click.prompt("Enter the start date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))
        end_date = click.prompt("Enter the end date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))
        
        if start_date > end_date:
            click.echo("The start date must be before the end date. Please try again.")
            return
        
        new_goal = ReadingGoal(goal=goal_number, start_date=start_date.date(), end_date=end_date.date(), status='active')
        db_session.add(new_goal)
        db_session.commit()
        click.echo("Your new reading goal has been set.")
    else:
        click.echo("No new reading goal added.")
    
    reading_goals_post_action_prompt()

@click.command()
def view_goal():
    goals = db_session.query(ReadingGoal).all()
    if goals:
        click.echo('Your Reading Goals:')
        for goal in goals:
            duration = (goal.end_date - goal.start_date).days
            if goal.goal > 0 :
                days_per_book = duration / goal.goal
                click.echo(f'Goal ID: {goal.id}, Read {goal.goal} books, '
                           f'Duration: {duration} days, '
                           f'Days per book: {days_per_book:.2f}, '
                           f'Start Date: {goal.start_date}, End Date: {goal.end_date}')
            else:
                click.echo(f'Goal ID: {goal.id} has 0 books set, unable to calculate days per book.')
    else:
        click.echo('No reading goals set.')
    
    reading_goals_post_action_prompt()

@click.command()
def edit_goal():
    goal_id = click.prompt('Enter the Reading Goal ID', type=int)
    goal = db_session.query(ReadingGoal).filter_by(id=goal_id).first()

    if goal:
        click.echo(f'Current Goal: Read {goal.goal} books from {goal.start_date} to {goal.end_date}')

        new_goal_number = click.prompt('Enter the new number of books', type=int)
        new_start_date = click.prompt('Enter the new start date (YYYY-MM-DD)', type=click.DateTime(formats=["%Y-%m-%d"]))
        new_end_date = click.prompt('Enter the new end date (YYYY-MM-DD)', type=click.DateTime(formats=["%Y-%m-%d"]))
        #new_status = click.prompt('Enter the new status (active, completed, failed) (or press Enter to keep current)', type=str, default=goal.status)

        goal.goal = new_goal_number
        goal.start_date = new_start_date
        goal.end_date = new_end_date
        #goal.status = new_status

        db_session.commit()
        click.echo('Reading Goal updated successfully.')
    
    else:
        click.echo('Reading Goal not found.')

    reading_goals_post_action_prompt()

@click.command()
def delete_goal():
    goal_id = click.prompt('Enter the Reading Goal ID', type=int)
    goal = db_session.query(ReadingGoal).filter_by(id=goal_id).first()

    if goal:
        db_session.delete(goal)
        db_session.commit()
        click.echo(f'Reading Goal {goal.id} deleted.')
    else:
        click.echo('Reading Goal not found.')

    reading_goals_post_action_prompt()

@click.group()
def review_mgt():
    review_mgt_menu()

@click.command()
def add_reviews():
  
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

    rating = click.prompt("Enter your rating (1-5)", type=float)
    review_text = click.prompt("Enter your review", default="", show_default=False)

    new_review = Review(book_id=selected_book.id, rating=rating, review=review_text)
    db_session.add(new_review)
    db_session.commit()
    click.echo(f'Review added for "{selected_book.name}".')

    reviews_mgt_post_action_prompt()

@click.command()
def view_reviews():
    reviews = db_session.query(Review).all()

    if reviews:
        click.echo('All Reviews:')
        for review in reviews:
            book_name = review.book.name if review.book else "Unknown Book"
            click.echo(f'Review ID: {review.id}, Book: {book_name}, Rating: {review.rating}, Notes: "{review.review}"')
    else:
        click.echo('No reviews found.')

    reviews_mgt_post_action_prompt()

@click.command()
def edit_reviews():
    # Prompt the user for the review ID
    review_id = click.prompt("Enter the Review ID to edit", type=int)
    
    # Fetch the review from the database
    review = db_session.query(Review).filter(Review.id == review_id).first()
    
    if review:
        # Show current review details
        click.echo(f"Current rating: {review.rating}")
        click.echo(f"Current review text: {review.review}")
        
        new_rating = click.prompt("Enter new rating (1-5)", type=int)
        new_review_text = click.prompt("Enter new notes", type=str)
        
        review.rating = new_rating
        review.review = new_review_text
        
        db_session.commit()
        click.echo("Review updated successfully.")
    else:
        click.echo("Review not found.")

    reviews_mgt_post_action_prompt()

@click.command()
def delete_reviews():
    review_id = click.prompt("Enter the Review ID to delete", type=int)
    
    review = db_session.query(Review).filter(Review.id == review_id).first()
    
    if review:
        db_session.delete(review)
        db_session.commit()
        click.echo(f"Review ID {review_id} deleted successfully.")
    else:
        click.echo("Review not found.")

    reviews_mgt_post_action_prompt()


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

#register commands
cli.add_command(add_book)
cli.add_command(view_books)
cli.add_command(update_status)
cli.add_command(delete_books)
#cli.add_command(update_goal)
cli.add_command(add_reviews)
cli.add_command(view_reviews)
cli.add_command(edit_reviews)
cli.add_command(delete_reviews)
cli.add_command(suggest_next)
cli.add_command(export_list)
cli.add_command(set_goal)
cli.add_command(view_goal)
cli.add_command(edit_goal)
cli.add_command(delete_goal)


def show_menu():
    click.echo('Welcome to LibLog!')
    click.echo('1: Manage Books')
    click.echo('2: Reading Goals')
    click.echo('3: Manage Reviews')
    click.echo('4: Book Suggestions')
    click.echo('5: Export Reading List')
    click.echo('6: Quit')
    
    while True:
        choice = click.prompt('Please enter your choice', type=int)

        if choice == 1:
            book_mgt_menu()
        elif choice == 2:
            reading_goal_menu()
        elif choice == 3:
            review_mgt_menu()
        elif choice == 4:
            suggest_next()
        elif choice == 5:
            export_list()
        elif choice == 6:
            click.echo('Goodbye!')
            sys.exit()
        else:
            click.echo('Invalid choice. Please choose a valid option.')

def reading_goal_menu():
    click.echo('Manage Reading Goals')
    click.echo('1: Set a reading goal')
    click.echo('2: View reading goals')
    click.echo('3: Edit reading goals')
    click.echo('4: Delete reading goals')
    click.echo('5: Main Menu')
    click.echo('6: Quit')

    while True:
        choice = click.prompt('Please enter your choice', type=int)

        if choice == 1:
            set_goal()
        elif choice == 2:
            view_goal()
        elif choice == 3:
            edit_goal()
        elif choice == 4:
            delete_goal()
        elif choice == 5:
            show_menu()
        elif choice == 6:
            click.echo('Goodbye!')
            sys.exit()
        else:
            click.echo('Invalid choice. Please choose a valid option.')

def book_mgt_menu():
    click.echo('Manage Books')
    click.echo('1: Add Book')
    click.echo('2: View Books')
    click.echo('3: Edit Books')
    click.echo('4: Delete Books')
    click.echo('5: Main Menu')
    click.echo('6: Quit')


    while True:
        choice = click.prompt('Please enter your choice', type=int)

        if choice == 1:
            add_book()
        elif choice == 2:
            view_books()
        elif choice == 3:
            update_status()
        elif choice == 4:
            delete_books()
        elif choice == 5:
            show_menu()
        elif choice == 6:
            click.echo('Goodbye!')
            sys.exit()

        else:
            click.echo('Invalid choice. Please choose a valid option.')

def review_mgt_menu():
    click.echo('Manage Reviews')
    click.echo('1: Add Reviews')
    click.echo('2: View Reviews')
    click.echo('3: Edit Reviews')
    click.echo('4: Delete Reviews')
    click.echo('5: Main Menu')
    click.echo('6: Quit')


    while True:
        choice = click.prompt('Please enter your choice', type=int)

        if choice == 1:
            add_reviews()
        elif choice == 2:
            view_reviews()
        elif choice == 3:
            edit_reviews()
        elif choice == 4:
            delete_reviews()
        elif choice == 5:
            show_menu()
        elif choice == 6:
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

def reading_goals_post_action_prompt():
    click.echo("\nWhat would you like to do next?")
    click.echo("1: Return to Reading Goals Menu")
    click.echo("2: Return to Main Menu")
    click.echo("3: Quit")
    choice = click.prompt("Please enter your choice", type=int)
    
    if choice == 1:
        reading_goal_menu()
    elif choice == 2:
        show_menu()
    else:
        click.echo('Goodbye!')
        sys.exit()

def book_mgt_post_action_prompt():
    click.echo("1: Return to Book Management Menu")
    click.echo("2: Return to Main Menu")
    click.echo("3: Quit")
    choice = click.prompt("Please enter your choice", type=int)
    
    if choice == 1:
        book_mgt_menu()
    elif choice == 2:
        show_menu()
    else:
        click.echo('Goodbye!')
        sys.exit()

def reviews_mgt_post_action_prompt():
    click.echo("1: Return to Reviews Management Menu")
    click.echo("2: Return to Main Menu")
    click.echo("3: Quit")
    choice = click.prompt("Please enter your choice", type=int)
    
    if choice == 1:
        review_mgt_menu()
    elif choice == 2:
        show_menu()
    else:
        click.echo('Goodbye!')
        sys.exit()


if __name__ == '__main__':
    show_menu() 
    # cli()