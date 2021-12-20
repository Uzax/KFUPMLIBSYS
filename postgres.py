import psycopg2 


# connect to DB 


def countbooks() :
    con = psycopg2.connect(
                 
                  database = "flaskapp",
                  user = "postgres"   
  
  
  )

    cur = con.cursor()
    cur.execute('select bid from  (select bid ,count(bid) as total from (SELECT "Borrower_Id" as bid  FROM public.book_loan where actual_return is null)  as totaltable  group by bid 	) as fina where total > 3 ;' )

    rows = cur.fetchall()

    #print(rows)

    ides = [] 
    for i in range(0 , len(rows)) :
        
        id = rows[i][0]

    
        cur.execute('select  req_id  from public.book_loan where "Borrower_Id" = '+ str(id)+' and actual_return is null ; ')

        rows2 = cur.fetchall() 
        for j in range(0 , len(rows2)): 
            req = rows2[j][0]
            cur.execute('select  (Current_date - borrowed_from ) as diff  from public.book_loan where req_id = '+str(req) +'  ; ')
            time = cur.fetchall() 

            for x in time:
                dif = str(x[0]).split(":")[0]
                dif = dif.split(" ")[0]
                #print(dif)
                if int(dif) > 120 : 
                    if id not in ides :
                        ides.append(id)
 


    cur.close()
    con.close()
    return ides





def totalpen(id) :
   con = psycopg2.connect(
                 
                  database = "flaskapp",
                  user = "postgres"   
  
  
  )
  
   cur = con.cursor()
   cur.execute('select people_id , sum(amount) from penalty where people_id = '+ str(id)+' group by people_id;')
   rows = cur.fetchall()
   
   #resu = "" 
#    for i in rows:
#        dif = str(i[1]).split(":")[0]
#        dif = dif.split(" ")[0]
   #resu = resu + rows[0][1]
       
    #    resu = resu + str(i[0])+" "+dif + " || "
  
  
   cur.close()
   con.close()
   return rows[0][1]





def panalty() : 
   con = psycopg2.connect(
                 
                  database = "flaskapp",
                  user = "postgres"   
  
  
  )
  
   cur = con.cursor()
   cur.execute('select "Borrower_Id",req_id ,(actual_return - borrowed_from) as inter from public.book_loan where (actual_return - borrowed_from) is not NULL;')
   rows = cur.fetchall()
   
   resu = "" 
   for i in rows:
       dif = str(i[2]).split(":")[0]
       dif = dif.split(" ")[0]
       
       #resu = resu + str(i[0]) + " " + str(i[1]) + " "+ str(dif) + " || "
   
       if int(dif) > 90  : 
         resu = resu + str(i[0])+" "+ str(i[1])+" "+str(int(dif) - 90) + " || "
  
  
   cur.close()
   con.close()
   return resu

 
def oneday():
 
 con = psycopg2.connect(
               
                database = "flaskapp",
                user = "postgres"   


)

 cur = con.cursor()
 cur.execute('select "Borrower_Id",actual_return - borrowed_from  as inter from public.book_loan where (actual_return - borrowed_from) is not NULL; ')
 rows = cur.fetchall()
 
 resu = "" 
 for i in rows:
     dif = str(i[1]).split(":")[0]
     dif = dif.split(" ")[0]
 
     if int(dif) < 90 and int(dif) > 0 : 
      resu = resu + str(i[0])+"-From Borrow to Return : "+str(dif) + " || "


 cur.close()
 con.close()
 return resu


#print(countbooks())


# CLose Connection 




