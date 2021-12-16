from flask import Flask , render_template , request 
from flask_sqlalchemy import SQLAlchemy 
from database import app , User , db 


@app.route('/')
def index() : 
    return render_template('index.html')

@app.route('/submit' , methods = ['POST'])
def login(): 
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        print(u + " " + p )

        USER = User.query.filter_by(username= u).first()
    
        if USER.password == p : 
            return render_template('suc.html')
        else :
            return render_template('index.html') 
        


if __name__ == '__main__': 
    app.debug = True 
    app.run()

