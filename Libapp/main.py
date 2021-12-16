from flask import Blueprint, render_template, flash , request
from flask_login import login_required, current_user
from __init__ import create_app, db
from models import User, book , Library_people ,People_type ,subject , author , book_item , book_loan , book_reserve , book_shelf

main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') 
@login_required
def profile():
    user = User.query.filter_by(username = current_user.username).first()
    people = Library_people.query.filter_by(people_id = user.people.people_id).first()

    return render_template('profile.html', name=people.First_name , type = people.actor.people_type)


@main.route('/search'  , methods=[ 'POST'])
def search():
    text = request.form.get('search')
    search_result = book.query.filter_by(title = text).first()
    data =[]
    data.append({'title': text})

    return render_template('search.html')
    
app = create_app() 
if __name__ == '__main__':
    db.create_all(app=create_app()) 
    app.run(debug=True) 