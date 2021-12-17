from flask import Blueprint, render_template, flash , request , url_for
from flask_login import login_required, current_user
from datetime import datetime
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

    if people.People_type_id == 2 : 
        return render_template('profile.html', name=people.First_name , type = people.actor.people_type)
    elif people.People_type_id == 1 : 
        return render_template('aprofile.html', name=people.First_name , type = people.actor.people_type)

@main.route('/search'  , methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET' : 
        return render_template('search.html')
    else : 
        selection = request.form.get('search_selction')
        text = request.form.get('searchbar')
        
        r = "" 
        if request.form.get('borrow_button') : 
            r = borrow(request.form.get('borrow_button').split(' ')[1])
            return render_template('search.html' , result = r)

        if request.form.get('reserve_button') : 
            r = reserve(request.form.get('reserve_button').split(' ')[1])
            return render_template('search.html' , result = r)





        if text is None : 
            return render_template('search.html')
        

        if selection == "ti":
            search_result = book.query.filter_by(book_title = text).all()

            if not search_result:
                return render_template('search.html' , result = "NO RESULT :(")
            else : 




                result1 = "" 
                for books in search_result : 
                    BorR = ""
                    if books.is_Available == "Y":
                        BorR = 'borrow'
                    else : 
                        BorR = 'reserve'
                    button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'

                    result1 = result1 + "Title: "+books.book_title + "  | Lang: " + books.book_language + '<br><br>' + button
                return render_template('search.html' , result = result1 )
        elif selection == "author":
      
            search_result = author.query.filter_by(name = text).first()

            if not search_result: 
                return render_template('search.html' ,result = "NO RESULT :(")
            else : 
                result1 = ""

                top = 7 
                for authors in search_result.book_author: 
                     books = book.query.filter_by(isbn_code = authors.isbn_code).first()
                    
                     BorR = ""
                     if books.is_Available == "Y":
                        BorR = 'borrow'
                     else : 
                        BorR = 'reserve'
                     
                     button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: '+str(top)+'%; left: 150%;"></input>'

                     result1 = result1 +" Title : " + books.book_title + " | Lang:" + books.book_language +'<br><br>' + button
                     top += 43

                return render_template('search.html' , result = result1)
        elif selection == "sub" : 
           
            search_result = subject.query.filter_by(subject_name = text).first() 

            if not search_result:  
                return render_template('search.html' ,result = "NO RESULT :(")

            else : 
                result1 = ""
        
                subject_books = book.query.filter_by(subject = search_result.subject_id).all()

                for books in subject_books:
                    BorR = ""
                    if books.is_Available == "Y":
                        BorR = 'borrow'
                    else : 
                        BorR = 'reserve'
                    button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'

                    result1 = result1 +" Title : " + books.book_title + " | Lang:" + books.book_language + '<br><br>' + button

                return render_template('search.html' , result = result1)

        elif selection == "pub" : 

            search_result = book.query.filter_by(publication_year = text).all()

            if not search_result: 
                    return render_template('search.html' )

            else :  

                result1 = "" 
                for books in search_result:
                    BorR = ""
                    if books.is_Available == "Y":
                        BorR = 'borrow'
                    else : 
                        BorR = 'reserve'
                    button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'

                    result1 = result1 +" Title : " + books.book_title + " | Lang:" + books.book_language + '<br><br>' + button

                return render_template('search.html' , result = result1)

        
        else:

            return render_template('search.html')




def borrow(ISBN):
    book_items = book_item.query.filter_by(isbn_code = ISBN).all() 
    availbe = False 
    for item in book_items: 
        print(item.status)
        if item.status == 'Y': 
            bcode = item.barcode 
            print(bcode)
            availbe = True 
            break

    if not availbe :  
        return "THERE is NO BOOK TO BORROW !!!!"
    
    user = User.query.filter_by(username = current_user.username).first()
    Today = current_Date() 
    add_borrwer = book_loan(Borrower_Id = user.people.people_id , book_barcode = bcode , borrowed_from = Today , borrowed_to = '20210101' , actual_return = None , issued_by= 2099999999 )
    db.session.add(add_borrwer) 
    db.session.query(book_item).filter(book_item.barcode == bcode).update({'status': 'N' })
    db.session.commit() 

    return "The Book ADDED"

def reserve(ISBN) : 
     user = User.query.filter_by(username = current_user.username).first()

     exist = book_reserve.query.filter_by(Borrower_Id = user.people.people_id , isbn_code = ISBN).first()

     if not exist : 
        add_reserve = book_reserve(Borrower_Id = user.people.people_id , isbn_code = ISBN , reserved_date = '20220101' , status = "Y")
        db.session.add(add_reserve) 
        db.session.commit() 
        return "THE BOOK RESERVED SUCC"
     else : 
        return "YOU ALREADY RESERVED IT "


@main.route('/books'  , methods=['GET', 'POST'])
@login_required
def books():
    if request.method == 'GET': 
        user = User.query.filter_by(username = current_user.username).first()

        search_result = book_loan.query.filter_by(Borrower_Id = user.people.people_id).all() 
    

        if not search_result : 
            return render_template('books.html' , result = "NO BOOKS")
        loc = -1250 


        result1 = "" 
        for borrowed in search_result :
            books_item = book_item.query.filter_by(barcode = borrowed.book_barcode).first()
            books  = book.query.filter_by(isbn_code = books_item.isbn_code).first()
            renew_button = '<input type="submit" name="renews_button" value="Renew '+borrowed.book_barcode+'" "="" style="width: 25%;height: 50px;position: absolute;top: '+str(loc)+'%;left: 70%;">'
            return_button = '<input type="submit" name="return_button" value="Return '+borrowed.book_barcode+'" "="" style="width: 25%;height: 50px;position: absolute;top: '+str(loc + 250)+'%;left: 70%;">'
            result1 = result1 + ' <h2 class="title" style="position: absolute;top: 25%;left: 20%;width: 70%;background-color: white;top: '+str(loc)+'%;left: -10%;height: 500%;font-size: 25px;position: absolute;right: 50%;text-align: left;"> Tilte: '+ books.book_title+'<br>'+'Borrowed From : '+str(borrowed.borrowed_from).split(' ')[0]+'</h2>'+ renew_button + return_button +'.'
            loc += 500 
    
        return render_template('books.html' , result = result1)
    else: 
        if request.form.get('renew_button') :
            #renew = book_loan.query.filter_by(book_barcode = request.form.get('renew_button').split(' ')[1]).first()
            Today = current_Date() 
            db.session.query(book_loan).filter(book_loan.book_barcode == request.form.get('renew_button').split(' ')[1]).update({'borrowed_from': Today })
            db.session.commit()
            return render_template('profile.html')
        elif request.form.get('return_button') :
            return_book = book_loan.query.filter_by(book_barcode = request.form.get('return_button').split(' ')[1]).first()
            db.session.query(book_item).filter(book_item.barcode == request.form.get('return_button').split(' ')[1]).update({'status': 'Y' })
            db.session.delete(return_book)
            db.session.commit() 
            return render_template('profile.html')



@main.route('/addbooks'  , methods=['GET', 'POST'])
@login_required
def addbooks(): 
    if request.method == 'GET': 

        return render_template('addbooks.html')
    
    if request.form.get('submit_btn') : 

        isbn = request.form.get('isbn')
        Title = request.form.get('title')
        lang = request.form.get('lang')
        
        selection = request.form.get('subject_selection')
        if selection == "none" : 
            new_subject = request.form.get('sub')
            new_sub = subject(subject_name = new_subject)
            db.session.add(new_sub)
            db.session.commit()
        elif selection == "CS" : 
            subjec = 101 
        elif selection == "DB" : 
            subjec = 102 
        elif selection == "DS" : 
            subjec = 103 


        avilav = request.form.get('av_selection')


        Year = request.form.get('year')
        copy_no = request.form.get('copy_no')


        new_book = book(isbn_code = isbn , book_title = Title , book_language = lang , 
        no_of_copies = copy_no , subject = subjec , is_Available = avilav , publication_year = Year )

        db.session.add(new_book)
        db.session.commit() 


        
        text = '<h3 style="font-weight: 900;position: absolute; left: 50%;top: 150%;font-size: 40px;"> DONE </h3>'

        return render_template('addbooks.html' , message = text )



        
        text = '<h3 style="font-weight: 900;position: absolute; left: 50%;top: 150%;font-size: 40px;"> DONE </h3>'





@main.route('/deletebook'  , methods=['GET', 'POST'])
@login_required
def deletebook(): 
    if request.method == 'GET': 

        return render_template('deletebooks.html')
    
    if request.form.get('submit_btn') : 

        isbn = request.form.get('isbn')
        
        delte_book = book.query.filter_by(isbn_code=isbn).first() 
        db.session.delete(delte_book)
        db.session.commit()


        
        text = '<h3 style="font-weight: 900;position: absolute;left: 50%;top: -150%;font-size: 40px;"> DONE </h3>'

        return render_template('deletebooks.html' , message = text )








def current_Date () : 

    date = str(datetime.utcnow()).split(' ')[0]
    date = date.split('-')
    date = date[0]+ date[1] + date[2]

    return date
    
app = create_app() 
if __name__ == '__main__':
    db.create_all(app=create_app()) 
    app.run(debug=True) 
