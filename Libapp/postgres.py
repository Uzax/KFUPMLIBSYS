import psycopg2 


# connect to DB 

con = psycopg2.connect(
               
                database = "flaskapp",
                user = "postgres"   


)


cur = con.cursor()



def signin(username): 

    username1 = "'{user}'".format(user = username)
    cur.execute('select password from "User" where username = {user}'.format(user = username1))
    rows = cur.fetchall()
    return rows[0][0]



cur.close()
# CLose Connection 
con.close()



