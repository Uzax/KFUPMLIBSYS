from flask import Blueprint, render_template, flash , request , url_for , redirect
from flask_login import login_required, current_user
from datetime import datetime , timedelta
from __init__ import create_app, db
from postgres import oneday , panalty , totalpen , countbooks
from models import User, book , Library_people ,People_type, penalty ,subject , author , book_item , book_loan , book_reserve , book_shelf 

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
        return render_template('profile.html', name=people.First_name )#, type = people.actor.people_type)
    elif people.People_type_id == 1 : 
        return render_template('aprofile.html', name=people.First_name )#, type = people.actor.people_type)
    elif people.People_type_id == 4 : 
        return render_template('admin_profile.html', name=people.First_name)
    else : 
        return render_template('index.html')

@main.route('/search'  , methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET' : 
        return render_template('search.html')
    else : 
        selection = request.form.get('search_selction')
        text = request.form.get('searchbar')
        
        r = "" 
        print(request.form.get('borrow_button'))
        if request.form.get('borrow_button') : 
            r = borrow(request.form.get('borrow_button'))
            return render_template('search.html' , result = r)

        if request.form.get('reserve_button') : 
            r = reserve(request.form.get('reserve_button'))
            return render_template('search.html' , result = r)





        if text is None : 
            return render_template('search.html')
        

        if selection == "ti":
            search_result = book.query.filter_by(book_title = text).all()

            if not search_result:
                return render_template('search.html' , result = '<span class="search-text18" style="top: 104%;"><span>NO RESULT :( </span><br><span></span><br><span></span></span>')
            else : 



                top = 104 
                result1 = ""
                for books in search_result : 
                    BorR = ""
                    availbe = book_item.query.filter_by(isbn_code = books.isbn_code).all()
                    status = False 
                    for item in availbe: 
                         if item.status == "Y":
                             status = True 
                             isbn = item.isbn_code 
                             break 
                    
                    
                    if status : # check st 
                         BorR = 'borrow'
                    else :
                         isbn = books.isbn_code
                         BorR = 'reserve'

                   # button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'

                    result1 = result1 + '<span class="search-text18" style="top: '+str(top)+'%;"><span>Title: '+books.book_title+'</span><br><span>LANG : '+ books.book_language  +'</span><br><span>SUBJECT</span></span> <button class="search-button2 button" style="top: '+str(top)+'%;" type="submit" name="'+BorR+'_button" id="'+BorR+'_button" value = "'+books.isbn_code+'">'+BorR+'</button>'  
                    top = top + 20 
                return render_template('search.html' , result = result1 )
        elif selection == "author":
      
            search_result = author.query.filter_by(name = text).first()

            if not search_result: 
                return render_template('search.html' ,result ='<span class="search-text18" style="top: 104%;"><span>NO RESULT :( </span><br><span></span><br><span></span></span>')
            else : 
                result1 = ""

                top = 0
                for authors in search_result.book_author: 
                     books = book.query.filter_by(isbn_code = authors.isbn_code).first()
                    
                     BorR = ""
                     availbe = book_item.query.filter_by(isbn_code = books.isbn_code).all()
                     status = False 
                     for item in availbe: 
                         if item.status == "Y":
                             status = True 
                             isbn = item.isbn_code 
                             break 
 
                    # button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'
                     if status :
                         BorR = 'borrow'
                     else :
                         isbn = books.isbn_code
                         BorR = 'reserve'
                     
                    # button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: '+str(top)+'%; left: 150%;"></input>'

                     result1 = result1 + '<span class="search-text18" style="top: '+str(top)+'%;"><span>Title: '+books.book_title+'</span><br><span>LANG : '+ books.book_language  +'</span><br><span>SUBJECT</span></span> <button class="search-button2 button" style="top: '+str(top)+'%;" type="submit" name="'+BorR+'_button" id="'+BorR+'_button" value = "'+books.isbn_code+'">'+BorR+'</button>'  
                     top += 20

                return render_template('search.html' , result = result1)
        elif selection == "sub" : 
           
            search_result = subject.query.filter_by(subject_name = text).first() 

            if not search_result:  
                return render_template('search.html' ,result = '<span class="search-text18" style="top: 104%;"><span>NO RESULT :( </span><br><span></span><br><span></span></span>')

            else : 
                result1 = ""

                subject_books = book.query.filter_by(subject = search_result.subject_id).all()
                top = 104 
                
                for books in subject_books:
                    BorR = ""
                    availbe = book_item.query.filter_by(isbn_code = books.isbn_code).all()
                    status = False 
                    for item in availbe: 
                        if item.status == "Y":
                            status = True 
                            isbn = item.isbn_code 
                            break 

                   # button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'
                    if status :
                        BorR = 'borrow'
                    else :
                        isbn = books.isbn_code
                        BorR = 'reserve'





                    result1 = result1 + '<span class="search-text18" style="top: '+str(top)+'%;"><span>Title: '+books.book_title+'</span><br><span>LANG : '+ books.book_language  +'</span><br><span>SUBJECT</span></span> <button class="search-button2 button" style="top: '+str(top)+'%;" type="submit" name="'+BorR+'_button" id="'+BorR+'_button" value = "'+isbn+'">'+BorR+'</button>'  
                    top = top + 20 
                return render_template('search.html' , result = result1)

        elif selection == "pub" : 

            search_result = book.query.filter_by(publication_year = text).all()

            if not search_result: 
                    return render_template('search.html' )

            else :  

                result1 = "" 
                top = 104 
                for books in search_result:
                   BorR = ""
                   availbe = book_item.query.filter_by(isbn_code = books.isbn_code).all()
                   status = False 
                   for item in availbe: 
                        if item.status == "Y":
                            status = True 
                            isbn = item.isbn_code 
                            break 
                   
                   
                   if status : # check st 
                        BorR = 'borrow'
                   else :
                        isbn = books.isbn_code
                        BorR = 'reserve'

                   # button = '<input type="submit" name="'+BorR+'_button"  value="'+BorR+' ' + books.isbn_code + '" " style=" width: 20%; height: 50px; position: absolute; top: 7%; left: 150%;"></input>'

                   result1 = result1 +  '<span class="search-text18" style="top: '+str(top)+'%;"><span>Title: '+books.book_title+'</span><br><span>LANG : '+ books.book_language  +'</span><br><span>SUBJECT</span></span> <button class="search-button2 button" style="top: '+str(top)+'%;" type="submit" name="'+BorR+'_button" id="'+BorR+'_button" value = "'+isbn+'">'+BorR+'</button>'  
                   top +=  66
                return render_template('search.html' , result = result1)

        
        else:

            return render_template('search.html')




@main.route('/report'  , methods=['GET', 'POST'])
@login_required
def report():
    user = User.query.filter_by(username = current_user.username).first()
    people = Library_people.query.filter_by(people_id = user.people.people_id).first()
    

    selection = request.form.get('report_select') 
    if selection == 'due' : 
        result = "" 
        res = oneday() 

        if len(res) > 0 :
           res = res.split('||')
           
           print(res)
           for i in range(0, len(res)-1) :
               m = res[i]
   
               
              
               sp = m.split('-')
               id = sp[0]
               id = int(id)
               
               
               info = Library_people.query.filter_by(people_id = id).first()
               result = result + "Name: " + info.First_name + " &nbsp;&nbsp; " + info.Last_name + " <br> ID:" + str(id) +"<br>"+ sp[1]+ " days <br><br>" 
               return render_template('admin_profile.html', name=people.First_name , output= result)
        else : return render_template('admin_profile.html', name=people.First_name , output= 'NO ONE ')
    elif selection == "pen" :
        result = "" 

        res = panalty()

        res = res.split('||')

        for i in range(0, len(res)-1): 
            m = res[i]

            sp = m.split(' ')
            id_p = sp[0]
            req = sp[1]
            days = int(sp[2])
            
            id_p = int(id_p)

            info = penalty.query.filter_by(req_id = req).first()

            if not info : 
                for j in range(0, 1000) :
                    check = penalty.query.filter_by(id = j).first()
                    if not check :
                        idd = j 
                        break 
                total = (days - 90 ) * 20 
                new_pen = penalty(id = idd , people_id = id_p  , req_id = req , amount = total)
                db.session.add(new_pen)
            else : 
                total = (days - 90) * 20 
                db.session.query(penalty).filter(penalty.req_id == req).update({'amount': total })

        db.session.commit() 

        people_ = Library_people.query.filter_by(People_type_id = 2).all()

        for p in people_ :
            pena = penalty.query.filter_by(people_id = p.people_id).first()
            if not pena : 

              result = result + "Name :" + p.First_name + " " + p.Last_name + "<br>Penalty = 0<br> ID :"+ str(p.people_id)+"<br>"
              continue
            else :
                total = totalpen(p.people_id) 
                result = result + "Name :" + p.First_name + " " + p.Last_name + "<br>Penalty = "+str(total) +"<br>ID :"+ str(p.people_id)+"<br>"


        return render_template('admin_profile.html', name=people.First_name , output= result)


    elif  selection == "boo" : 
        ides = countbooks()

        res = "" 

        for i in ides : 
            people_ = Library_people.query.filter_by(people_id= i ).first() 

            res = res + "Name : " + people_.First_name + " " + people_.Last_name + "<br>" + "ID: " + str(i) + "<br><br>"

        
        return render_template('admin_profile.html', name=people.First_name , output= res)


    elif selection == "new":

        new_people = Library_people.query.filter_by(added_Year = '2021').all()

        res = "" 
        for p in new_people :
            check = book_loan.query.filter_by(Borrower_Id = p.people_id).first()

            if not check :
                res=res + "Name : " + p.First_name + " " + p.Last_name +"<br>ID : "+ str(p.people_id)+"<br<br>"
            
        return render_template('admin_profile.html', name=people.First_name , output= res)












        
        


    return render_template('admin_profile.html', name=people.First_name , output= "Good <br> Morning")



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
        return '<span class="search-text18" style="top: 104%;"><span>THERE is NO BOOK TO BORROW !!!!</span><br><span></span><br><span></span></span>'
    
    user = User.query.filter_by(username = current_user.username).first()
    
    for em in range(0 , 1000):
        emp = book_loan.query.filter_by(req_id = em).first()
        if not emp : 
            index = em 
            break 

    Today = current_Date() 
    future = dayes90()
    add_borrwer = book_loan(req_id = index , Borrower_Id = user.people.people_id , book_barcode = bcode , borrowed_from = Today , borrowed_to = future , actual_return = None , issued_by= 2099999999 )
    db.session.add(add_borrwer) 
    db.session.query(book_item).filter(book_item.barcode == bcode).update({'status': 'N' })
    db.session.commit() 

    return '<span class="search-text18" style="top: 104%;"><span>The Book ADDED</span><br><span></span><br><span></span></span>'
    

def reserve(ISBN) : 
     user = User.query.filter_by(username = current_user.username).first()

     exist = book_reserve.query.filter_by(Borrower_Id = user.people.people_id , isbn_code = ISBN).first()

     if not exist : 
        add_reserve = book_reserve(Borrower_Id = user.people.people_id , isbn_code = ISBN , reserved_date = '20220101' , status = "Y")
        db.session.add(add_reserve) 
        db.session.commit() 
        return '<span class="search-text18" style="top: 104%;"><span>THE BOOK RESERVED SUCC</span><br><span></span><br><span></span></span>'
     else : 
        return '<span class="search-text18" style="top: 104%;"><span>YOU ALREADY RESERVED IT </span><br><span></span><br><span></span></span>'


@main.route('/books'  , methods=['GET', 'POST'])
@login_required
def books():
    if request.method == 'GET': 
        user = User.query.filter_by(username = current_user.username).first()

        search_result = book_loan.query.filter_by(Borrower_Id = user.people.people_id , actual_return = None).all() 

        search_result_reserve = book_reserve.query.filter_by(Borrower_Id = user.people.people_id).all()
    

        if not search_result :  # BOOROW
           result1 = 'NO BOOKS'
        else : 
            loc = 0
            result1 = "" 
            for borrowed in search_result :
                
                books_item = book_item.query.filter_by(barcode = borrowed.book_barcode).first()
                books  = book.query.filter_by(isbn_code = books_item.isbn_code).first()
                renew_button = ' <button type="submit" name="renew_button" value="'+borrowed.book_barcode+'" class="books-button1 button" style="left: 60%; top: ' + str(loc)+'%;">Renew</button>'
                return_button = ' <button type="submit" name="return_button" value="'+borrowed.book_barcode+'" class="books-button1 button" style="left: 60%; top: ' + str(loc+20)+'%;">Return</button>'

                date = str(borrowed.borrowed_from).split(' ')[0]
                result1 = result1 + 'Title : '+books.book_title+'<br>Borrowed From : '+date + renew_button + return_button + '<br><br>'
                
                loc += 40
        

        if not search_result_reserve :  # RESERVED 
            result2 = 'Empty'
        else : 
            loc = 0
            button_loc = 0 
            result2 = ""
            for reserved in search_result_reserve : 
                books= book.query.filter_by(isbn_code = reserved.isbn_code).first()
                cance_button = ' <button type="submit" name="cancel_button" value="'+reserved.isbn_code+'" class="books-button1 button" style="left: 60%; top: ' + str(button_loc)+'%;">Cancel</button>'
                result2 = result2 + 'Title: '+books.book_title+'<br>Reserved Date : '+str(reserved.reserved_date).split(' ')[0]+'<br>Status : '+reserved.status+ cance_button+ '<br><br>'
                loc += 40 
                button_loc += 50


        return render_template('books.html' ,result = result1 , reserv = result2)

    else: 
        if request.form.get('renew_button') :
            #renew = book_loan.query.filter_by(book_barcode = request.form.get('renew_button').split(' ')[1]).first()
            print("Hi")
            Today = current_Date() 
            db.session.query(book_loan).filter(book_loan.book_barcode == request.form.get('renew_button')).update({'borrowed_from': Today })
            db.session.commit()
            return render_template('search.html')
        elif request.form.get('return_button') :
            print ('in')
            Today =current_Date()
            db.session.query(book_loan).filter(book_loan.book_barcode == request.form.get('return_button')).update({'actual_return' : Today})
            db.session.query(book_item).filter(book_item.barcode == request.form.get('return_button')).update({'status': 'Y' })
            db.session.commit() 
            return render_template('search.html')
        elif request.form.get('cancel_button'):
            user = User.query.filter_by(username = current_user.username).first()
            dele_res = book_reserve.query.filter_by(Borrower_Id = user.people.people_id , isbn_code = request.form.get('cancel_button')).first()
            db.session.delete(dele_res)
            db.session.commit()
            return render_template('search.html')




@main.route('/addbooks'  , methods=['GET', 'POST'])
@login_required
def addbooks(): 
    if request.method == 'GET': 
        subjects = subject.query.all() 

        option = "" 
        for sub in subjects: 
            option = option + ' <option value="'+str(sub.subject_id) + '">'+sub.subject_name+'</option>'

        return render_template('addbooks.html' , op = option)
    
    if request.form.get('submit_add') : 

        isbn = request.form.get('isbn')
        Title = request.form.get('title')
        lang = request.form.get('lang')
        
        selection  = request.form.get('subject_selection')
        print(selection)
        if selection == "none" : 
            new_subject = request.form.get('sub')
            for i in range(0, 1000):
                che = subject.query.filter_by(subject_id = i).first()
                if not che : 
                    sub_id = i 
                    break 

            new_sub = subject(subject_id = sub_id , subject_name = new_subject)
            db.session.add(new_sub)
            db.session.commit()
            get_id_sub = subject.query.filter_by(subject_name = new_subject).first()
            subjec = get_id_sub.subject_id 
        else : 
            subjec = int(selection)

      


        avilav = request.form.get('avl')


        Year = request.form.get('year')
        copy_no = request.form.get('nocopy')

        #print(isbn , Title, lang  ,avilav , Year , copy_no )


        

        new_book = book(isbn_code = isbn , book_title = Title , book_language = lang , 
         no_of_copies = copy_no , subject = subjec , is_Available = avilav , publication_year = Year )

        db.session.add(new_book)
        db.session.commit() 


        
        # text = '<h3 style="font-weight: 900;position: absolute; left: 50%;top: 150%;font-size: 40px;"> DONE </h3>'

        return render_template('aprofile.html' , message = "ADDED :) " )
    
    #return render_template('addbooks.html' , message = "no" )


        
       # text = '<h3 style="font-weight: 900;position: absolute; left: 50%;top: 150%;font-size: 40px;"> DONE </h3>'





@main.route('/deletebook'  , methods=['GET', 'POST'])
@login_required
def deletebook(): 
    if request.method == 'GET': 

        return render_template('deletebooks.html')
    
    if request.form.get('submit_btn') :



        isbn = request.form.get('isbn')
        
        delte_book = book.query.filter_by(isbn_code=isbn).first() 


        if not delte_book : 
            text = ' <h1 class="deletebook-text6"><span>WRONG ISBN </span><span class="deletebook-text8"></span></h1>'
            return render_template('deletebooks.html' , message = text )

        delte_items = book_item.query.filter_by(isbn_code=isbn).all() # NEW 

        for item in delte_items :  
            db.session.delete(item)

        db.session.delete(delte_book)
        db.session.commit()


        
        text = ' <h1 class="deletebook-text6"><span>DONE</span><span class="deletebook-text8"></span></h1>'

        return render_template('deletebooks.html' , message = text )






@main.route('/editbook'  , methods=['GET', 'POST'])
@login_required
def editbook(): 
    button_search = '<input type="text" id="isbn1" name="isbn1" placeholder="ISBN" class="editbook-textinput7 input"/>'
    if request.method == 'GET': 

        return render_template('editbook.html' , button = button_search)
    else :
       
        if request.form.get('submit_search') : 
 
            isbn = request.form.get('isbn1')
 
            
            search_book = book.query.filter_by(isbn_code=isbn).first()

            if not search_book : 
                 txt = '<h1 class="editbook-text20"><span>NOT AVAILABLE</span></h1>'
                 return render_template('editbook.html' , notresult = txt , button = button_search )
                 

            subj = subject.query.filter_by(subject_id = search_book.subject).first()
            form2 = ' <form class="editbook-form"   action="/editbook" method="POST" style="left: 43%; top: 11%;" > <input id="submit_edit" name="submit_edit" type="submit" value = "SUBMIT" class="editbook-button button"> <input  type="text"  id="title"   name="title" value="'+search_book.book_title+'" placeholder="Title" class="editbook-textinput input"/><input  type="text"  id="sub"  name="sub" value="'+subj.subject_name+'"  placeholder="Subject"  class="editbook-textinput1 input"/><input  type="text"  id="nocopy"  name="nocopy" value="'+str(search_book.no_of_copies)+'"  placeholder="COPY"  class="editbook-textinput2 input"/><input  type="text"  id="lang"  name="lang" value="'+search_book.book_language+'" placeholder="Language"  class="editbook-textinput3 input"/>  <input    type="text"    id="avl"    name="avl"    value="'+search_book.is_Available+'" placeholder="Y OR N"    class="editbook-textinput4 input"  />  <input    type="text"    id="year"    name="year"   placeholder="Year"  value="'+str(search_book.publication_year)+'"  class="editbook-textinput5 input"  />  <input    type="text"    id="isbn"    name="isbn"  value="'+search_book.isbn_code+'"  placeholder="ISBN"    class="editbook-textinput6 input"  /> <input    type="hidden"    id="isbn1"    name="isbn1"  value="'+search_book.isbn_code+'"  placeholder="ISBN"    class="editbook-textinput6 input"  />      <label class="editbook-text04">Subject :</label>         <label class="editbook-text05">No Copy :</label>         <label class="editbook-text06">is Available ? (Y/N)</label>         <label class="editbook-text07">Year :</label>         <label class="editbook-text08">Language :</label>         <label class="editbook-text09">Book Title :</label>         <label class="editbook-text10"><span>ISBN Code :</span></label>     <h1 class="editbook-text12">    <span>DONE</span>    <span class="editbook-text14"></span>  </h1></form>'

            new_button = '<input type="text" id="isbn1" name="isbn1" value="'+isbn+'" placeholder="ISBN" class="editbook-textinput7 input"/>'
            return render_template('editbook.html' , result = form2  , button = new_button )

        if request.form.get('submit_edit') : 
              isbn = request.form.get('isbn1')
              isbn1 = request.form.get('isbn')
              Title = request.form.get('title')
              lang = request.form.get('lang')
              subjec = request.form.get('sub')
              copies = request.form.get('nocopy')
              avilable = request.form.get('avl')
              year = request.form.get('year')

             
              #db.session.query(book).filter(book.isbn_code == isbn).update({'isbn_code': isbn1  , 'book_title' : Title , 'book_language' : lang , 'no_of_copies' : int(copies) , 'is_Available' : avilable , 'publication_year' : year})
              udate = book.query.filter_by(isbn_code = isbn).first()
              udate.isbn_code = isbn1
              udate.book_title = Title 
              udate.book_language = lang 
              udate.publication_year = year
              udate.no_of_copies = copies 
              udate.is_Available = avilable 

              db.session.commit()

              txt = '<h1 class="editbook-text20"><span>DONE </span></h1>'
              return render_template('editbook.html' , notresult = txt  , button = button_search)



    #print (isbn)
        # delte_book = book.query.filter_by(isbn_code=isbn).first() 
        # db.session.delete(delte_book)
        # db.session.commit()


        
   # text = '<h3 style="font-weight: 900;position: absolute;left: 50%;top: -150%;font-size: 40px;"> DONE </h3>'

    #return render_template('editbook.html'  )


@main.route('/additem'  , methods=['GET', 'POST'])
@login_required
def additem(): 
    if request.method == 'GET': 
        return render_template('additem.html')

    if request.form.get('submit_add') :
        isbn   = request.form.get('isbn')
        barcode   = request.form.get('bar')
        copies = request.form.get('nocopy')
        avl = request.form.get('avl')

        search_result = book.query.filter_by(isbn_code = isbn).first()

        if not search_result : 
            txt = '<span style="top: 52%;position: absolute;left: 30%;"><span>THERE IS NO BOOK WITH THAT ISBN </span><br><span></span><br><span></span></span>'
            return render_template('additem.html' , result = txt)

        new_item = book_item(isbn_code = isbn, barcode = barcode, book_copy_no = copies, status =avl)
        db.session.add(new_item)
        db.session.commit()
        
        txt = '<span style="top: 52%;position: absolute;left: 30%;"><span>DONE </span><br><span></span><br><span></span></span>'
        return render_template('additem.html' , result = txt)

         

    

@main.route('/deleteitem'  , methods=['GET', 'POST'])
@login_required
def deleteitem(): 
    if request.method == 'GET': 

        return render_template('deleteitem.html')
    
    if request.form.get('submit_btn') :



        Barcode = request.form.get('bar')
        
        delete_item = book_item.query.filter_by(barcode=Barcode).first() 


        if not delete_item : 
            text = ' <h1 class="deletebook-text6"><span>WRONG BARCODE </span><span class="deletebook-text8"></span></h1>'
            return render_template('deleteitem.html' , message = text )

        db.session.delete(delete_item)
        db.session.commit()


        
        text = ' <h1 class="deletebook-text6"><span>DONE</span><span class="deletebook-text8"></span></h1>'

        return render_template('deleteitem.html' , message = text )



@main.route('/edititem'  , methods=['GET', 'POST'])
@login_required
def edititem(): 
    button_search = '<input type="text" id="bar1" name="bar1" placeholder="barcode" class="editbook-textinput7 input"/>'
    if request.method == 'GET': 

        return render_template('edititem.html' , button = button_search)
    else :
       
        if request.form.get('submit_search') : 
 
            Barcode = request.form.get('bar1')

            print(Barcode)
            
            search_book = book_item.query.filter_by(barcode=Barcode).first()

            if not search_book : 
                 txt = '<h1 class="editbook-text20"><span>NOT AVAILABLE</span></h1>'
                 return render_template('edititem.html' , notresult = txt , button = button_search )
                 

            if search_book.isbn_code == None :
                isbn_c = 'Null'

            else : 
                isbn_c = search_book.isbn_code
            form2 = '<form class="editbook-form" action="/edititem" method="POST" style="left: 43%; top: 11%;"> <input id="submit_edit" name="submit_edit" type="submit" value="SUBMIT" class="editbook-button button"> <input type="text" id="bar" name="bar" value="'+search_book.barcode+'" placeholder="Barcode" class="editbook-textinput input"><input type="text" id="avl" name="avl" value="'+search_book.status+'" placeholder="Subject" class="editbook-textinput1 input"><input type="text" id="copy_no" name="copy_no" value="'+str(search_book.book_copy_no)+'" placeholder="Language" class="editbook-textinput3 input">      <input type="text" id="isbn" name="isbn" value="'+isbn_c+'" placeholder="ISBN" class="editbook-textinput6 input"> <input type="hidden" id="bar1" name="bar1" value="'+search_book.barcode+'" placeholder="ISBN" class="editbook-textinput6 input">      <label class="editbook-text04">Status :</label>                                    <label class="editbook-text08">Copy_No :</label>         <label class="editbook-text09">Barcode :</label>         <label class="editbook-text10"><span>ISBN :</span></label>     <h1 class="editbook-text12">    <span></span>    <span class="editbook-text14"></span>  </h1></form>'
            #form2 = '<form class="editbook-form" action="/edititem" method="POST" style="left: 43%; top: 11%;"> <input id="submit_edit" name="submit_edit" type="submit" value="SUBMIT" class="editbook-button button"> <input type="text" id="bar" name="bar" value="'+search_book.barcode+'" placeholder="Barcode" class="editbook-textinput input"><input type="text" id="avl" name="avl" value="'+search_book.status+'" placeholder="Subject" class="editbook-textinput1 input"><input type="text" id="copy_no" name="copy_no" value="'+str(search_book.book_copy_no)+'" placeholder="Language" class="editbook-textinput3 input">      <input type="text" id="isbn" name="isbn" value="" placeholder="ISBN" class="editbook-textinput6 input"> <input type="hidden" id="bar1" name="bar1" value="82" placeholder="ISBN" class="editbook-textinput6 input">      <label class="editbook-text04">Status :</label>                                    <label class="editbook-text08">Copy_No :</label>         <label class="editbook-text09">Barcode :</label>         <label class="editbook-text10"><span>ISBN Code :</span></label>     <h1 class="editbook-text12">    <span>DONE</span>    <span class="editbook-text14"></span>  </h1></form>'
            new_button = '<input type="text" id="bar1" name="bar1" value="'+Barcode+'" placeholder="ISBN" class="editbook-textinput7 input"/>'
            return render_template('editbook.html' , result = form2  , button = new_button )

        if request.form.get('submit_edit') : 
              old_barcode = request.form.get('bar1')
              isbn = request.form.get('isbn')
              barcode = request.form.get('bar')
              copies = request.form.get('copy_no')
              avilable = request.form.get('avl')

             
              #db.session.query(book).filter(book.isbn_code == isbn).update({'isbn_code': isbn1  , 'book_title' : Title , 'book_language' : lang , 'no_of_copies' : int(copies) , 'is_Available' : avilable , 'publication_year' : year})
              
              check = book.query.filter_by(isbn_code = isbn).first()

              if not check : 
                  txt = '<h1 class="editbook-text20"><span>Wrong ISBN </span></h1>'
              else : 
                     
                 udate = book_item.query.filter_by(barcode = old_barcode).first()
                 udate.isbn_code = isbn
                 udate.barcode = barcode 
                 udate.book_copy_no = copies 
                 udate.status = avilable 
   
                 db.session.commit()
   
                 txt = '<h1 class="editbook-text20"><span>DONE </span></h1>'
              return render_template('editbook.html' , notresult = txt  , button = button_search)




@main.route('/new_member'  , methods=['GET', 'POST'])
@login_required
def new_member(): 
     if request.method=='GET': 
        return render_template('new_member.html')
     else: 
        #if request.form.get('signup') : 
          fname = request.form.get('fname')
          lname  = request.form.get('lname')
          pid  = request.form.get('pid')        
          sex  = request.form.get('sex')
          dob  = request.form.get('dob').split('-')
          dob = dob[0]+dob[1]+dob[2]
          phone  = request.form.get('phone')
          username  = request.form.get('user')
          password = request.form.get('password')

          people = Library_people.query.filter_by( people_id = pid ).first() 

          if people : 
              return render_template('new_member.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">ID ALREADY EXSIT</label>')
          
          user = User.query.filter_by(username=username).first() 
          if user: 
              return render_template('new_member.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">Username ALREADY EXSIT</label>')

          new_people = Library_people(people_id = int(pid) , First_name = fname , Last_name = lname ,People_type_id = 2, Date = dob , Sex = sex ,Contact_Number = phone , added_Year = '2021')
          db.session.add(new_people)
          db.session.commit()
          
          id = 99999
          for i in range(0, 100):
              find = User.query.filter_by(id = i).first()
              if not find :
                  id = i 
                  break 
          print("HERE")
          new_user = User(id = id , username = username , password = password , people_id = int(pid))
          db.session.add(new_user)
          db.session.commit()

          return render_template('new_member.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">ADDED :) </label>')



@main.route('/delete_member'  , methods=['GET', 'POST'])
@login_required
def delete_member(): 
     if request.method == 'GET': 

        return render_template('delete_member.html')
    
     if request.form.get('submit_btn') :



        id = request.form.get('id')
        
        delete_member = Library_people.query.filter_by(people_id=id).first() 


        if not delete_member : 
            text = ' <h1 class="deletebook-text6"><span>WRONG BARCODE </span><span class="deletebook-text8"></span></h1>'
            return render_template('delete_member.html' , message = text )

        delete_user = User.query.filter_by(people_id = id).first()
        db.session.delete(delete_user)

        delete_borrowed_book = book_loan.query.filter_by(Borrower_Id = id).all()

        for b in delete_borrowed_book : 
            db.session.delete(b)

        delete_res = book_reserve.query.filter_by(Borrower_Id = id).all()

        for r in delete_res : 
            db.session.delete(r)

                
        
        db.session.delete(delete_member)
        db.session.commit()


        
        text = ' <h1 class="deletebook-text6"><span>DONE</span><span class="deletebook-text8"></span></h1>'

        return render_template('deleteitem.html' , message = text )

def current_Date () : 

    date = str(datetime.utcnow()).split(' ')[0]
    date = date.split('-')
    date = date[0]+ date[1] + date[2]

    return date


def dayes90 () : 

    date = str(datetime.now() + timedelta(days=90)).split(' ')[0]
    date = date.split('-')
    date = date[0]+ date[1] + date[2]

    return date
    
app = create_app() 
if __name__ == '__main__':
    db.create_all(app=create_app()) 
    app.run(debug=True) 