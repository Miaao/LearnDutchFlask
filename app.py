from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


#create and connect to database
DATABASE = 'myapp.db'
def connect_db():
    return sqlite3.connect(DATABASE)


#create index url & function mapping for root or / (index page)
@app.route('/')
def index():
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence from people')
    entries = [dict(id = row[0], myname = row[1], country_of_residence = row[2]) for row in cur.fetchall()]
    print(entries)
    db.close()
    return render_template('ProfileList.html', entries = entries)
    #return"Hello from Flask!"

#create routing for myProfile
@app.route('/myprofile')
def showmyprofile():
    return render_template('MyProfile.html')

#create mapping to show the form for /addprofile
@app.route('/addprofileform')
def addprofileform():
    return render_template('MyProfileForm.html')

#create a mapping for /addprofile
@app.route('/addprofile')
def addprofile():
    myname = request.args.get('myname')
    country_of_residence = request.args.get('country_of_residence')
    db = connect_db()
    sql = 'insert into people (myname, country_of_residence) values (?,?)'
    db.execute(sql, [myname, country_of_residence])
    db.commit()
    db.close()
    return render_template('MyProfile.html', myname = myname, country_of_residence = country_of_residence)

#update profile
@app.route('/editprofile')
def editprofile():
    id = request.args.get('id')
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence from people where id=?',[id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    print(rv[0])
    db.close()
    return render_template('MyProfileUpdateForm.html', person=person)

#update profile
@app.route('/updateprofile')
def updateprofile():
    id = request.args.get('id')
    myname = request.args.get('myname')
    country_of_residence = request.args.get('country_of_residence')
    db = connect_db()
    sql = 'update people set myname=?, country_of_residence=? where id=?'
    db.execute(sql, [myname,country_of_residence,id])
    db.commit()
    db.close()
    return index()

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True )