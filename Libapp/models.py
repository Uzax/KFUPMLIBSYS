from collections import UserList
from flask_login import UserMixin
from __init__ import db , app 


class Library_people(db.Model): 
    people_id = db.Column(db.Integer , primary_key=True) 
    First_name = db.Column(db.String(20) , nullable= False)
    Last_name = db.Column(db.String(20) , nullable= False)
    People_type_id = db.Column(db.Integer , db.ForeignKey('people_type.id') , nullable = False)
    Date = db.Column(db.DateTime)
    Sex = db.Column(db.String(1) , nullable = True)
    Department = db.Column(db.String(5) , nullable= True)
    Contact_Number = db.Column(db.String(13) , nullable= True)
    people_username = db.relationship('User' , backref = 'people')
    people_book = db.relationship('book_loan' , backref = 'book_people' , foreign_keys = 'book_loan.Borrower_Id')
    people_book2 = db.relationship('book_loan' , backref = 'book_people2' , foreign_keys= 'book_loan.issued_by')
    people_reserve = db.relationship('book_reserve' , backref = 'bookresev')


class User(UserMixin,db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20) , unique = True)
    password = db.Column(db.String(20), nullable=False )
    people_id = db.Column(db.Integer , db.ForeignKey('library_people.people_id'))

class People_type(db.Model):
    id = db.Column(db.Integer , primary_key=True) 
    people_type = db.Column(db.String(15), nullable= False)
    peoplerel = db.relationship('Library_people' , backref = 'actor')


class subject(db.Model):
  __tablename__ = "subject"
  subject_id = db.Column(db.Integer, primary_key=True)
  subject_name = db.Column(db.String(50))
  book_subject = db.relationship('book' , backref = 'book_subject')
  def __repr__(self):
    return f'<subject {self.subject_id} {self.subject_name}>'




book_auth = db.Table('book_author' , 
    db.Column('isbn_code' ,db.String(10) , db.ForeignKey('book.isbn_code')) ,
    db.Column('author_id' ,db.Integer , db.ForeignKey('author.author_id'))) 
  
class book(db.Model):
  __tablename__ = "book"
  isbn_code = db.Column(db.String(10), primary_key=True) #
  book_title = db.Column(db.String(70))
  book_language = db.Column(db.String(20))
  no_of_copies = db.Column(db.Integer)
  subject = db.Column(db.Integer , db.ForeignKey('subject.subject_id'))
  is_Available = db.Column(db.String(1))
  publication_year = db.Column(db.Integer)
  bookItem = db.relationship('book_item' , backref= 'book' ,cascade="all, delete-orphan")
  book_reserved = db.relationship('book_reserve', backref= 'bookreserv' , cascade="all, delete-orphan")
  authors = db.relationship('author', secondary = book_auth ,backref = db.backref('book_author' , lazy = 'dynamic'))



  def __repr__(self):
    return f'<Book {self.isbn_code} {self.book_title} {self.is_Available}>'





class author(db.Model): 
    author_id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(30))
    DOB = db.Column(db.DateTime)
    




#class book_author (db.Model):  # NOT DONE 
 #   author_id = db.Column(db.Integer , primary_key = True)

class book_item(db.Model) :
    barcode = db.Column(db.String(12) , primary_key=True)
    isbn_code = db.Column(db.String(10) , db.ForeignKey('book.isbn_code'))
    book_copy_no = db.Column(db.Integer , nullable = False)
    status = db.Column(db.String(1))
    loanbarcode = db.relationship('book_loan' , backref = 'loanbarcode')



class book_loan(db.Model): 
    Borrower_Id = db.Column(db.Integer, db.ForeignKey('library_people.people_id') , primary_key=True)
    book_barcode =  db.Column(db.String(12), db.ForeignKey('book_item.barcode') , primary_key=True)
    borrowed_from = db.Column(db.DateTime , nullable = False , primary_key=True)
    borrowed_to = db.Column(db.DateTime, nullable= False)
    actual_return = db.Column(db.DateTime)
    issued_by = db.Column(db.Integer, db.ForeignKey('library_people.people_id') , primary_key=True)



class book_reserve(db.Model):
    Borrower_Id = db.Column(db.Integer, db.ForeignKey('library_people.people_id') , primary_key=True)
    isbn_code = db.Column(db.String(10), db.ForeignKey('book.isbn_code'), primary_key=True)
    reserved_date = db.Column(db.DateTime)
    status = db.Column(db.String(1))


class book_shelf(db.Model):
    sheld_id = db.Column(db.Integer , primary_key=True)
    shelf_no = db.Column(db.String(4))
    floor_no = db.Column(db.Integer)
    





   




#with app.app_context():
    #db.drop_all()
   #db.create_all()
   ##test = author.query.filter_by(name='bader').first()

  ## for books in test.book_author: 
         ##print(books.isbn_code)
    
    #book_items = book_item.query.filter_by().all()

################################################################
   # db.session.query(book_item).filter(book_item.barcode == '988849434943').update({'status': 'Y'})
    #db.session.commit() 
   ################# 
    #for books in test.author.book_author :
    #    print(books.isbn_code)
   # print(test2.book_author.isbn_code
