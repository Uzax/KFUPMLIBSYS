from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User , Library_people 
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

auth = Blueprint('auth', __name__) 

@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        return render_template('login.html')
    else: 
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
       
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username = username).first()
       
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif user.password != password:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method=='GET': 
        return render_template('signup.html')
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
              return render_template('signup.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">ID ALREADY EXSIT</label>')
          
          user = User.query.filter_by(username=username).first() 
          if user: 
              return render_template('signup.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">Username ALREADY EXSIT</label>')

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

          return render_template('signup.html' , result = '<label class="signup-text4" style="left: 31%;top: 6%;color: red;font-weight: bold;">YOU CAN LOGIN NOW</label>')


       # return redirect(url_for('auth.login'))

        # new_user = User(username=username, email=email, password=password) #
        # # add the new user to the database
        # db.session.add(new_user)ç
        # db.session.commit()
        

@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('auth.login'))