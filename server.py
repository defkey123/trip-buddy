from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
import datetime

app = Flask(__name__)
app.secret_key = "lol secrect key am i rite"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route("/emailconfirm", methods=["post"])
def username():
    found = False
    mysql = connectToMySQL('trip_buddy')
    query = "SELECT email from users WHERE users.email = %(em)s;"
    data = { 'em' : request.form['email'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('emailconfirm.html', found=found)

@app.route('/register', methods=["post"])
def register():
    mysql=connectToMySQL('trip_buddy')
    data = {
    "fn" : request.form["firstname"],
    "ln" : request.form["lastname"],
    "em" : request.form["email"],
    "pw" : request.form["password"],
    "pw_cnf" : request.form["password_confirm"],
    }
    err = []
    if len(data['fn']) < 2:
        err.append("First name needs to be at least 2 characters")
    if len(data['ln']) < 2:
        err.append("Username needs to be at least 2 characters")
    if not EMAIL_REGEX.match(data['em']):
        err.append("Email address is invalid")
    if len(data['pw']) < 8:
        err.append("Password needs to be at least 8 characters")
    if not data['pw'] == data['pw_cnf']:
        err.append("Passwords don't match")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        data['pw'] = bcrypt.generate_password_hash(data['pw'])
        query = "INSERT INTO users (first_name, last_name, email, password_hash) VALUES ( %(fn)s, %(ln)s, %(em)s, %(pw)s )"
        query_result = mysql.query_db(query, data)
        session['firstname'] = data["fn"]
        session['uid'] = query_result
        return redirect('/trips')

    return redirect('/')

@app.route('/login', methods=["post"])
def login():
    mysql = connectToMySQL('trip_buddy')

    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form['email'], "password" : request.form['password']}
    print(data)
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
            session['uid'] = result[0]['id']
            session['firstname'] = result[0]["first_name"]
            return redirect('/trips')

    flash("Login failed. Please check your credentials.")
    return redirect('/')

@app.route('/log_out')
def log_out():
    print("logging out...")
    session.clear()
    return redirect('/')

@app.route('/trips')
def trips():
    if not 'uid' in session:
        return redirect('/')
    mysql = connectToMySQL('trip_buddy')
    query = 'SELECT * FROM trips JOIN users WHERE users.id = trips.created_by'
    all_trips = mysql.query_db(query)
    return render_template("trips.html", trips=all_trips)

@app.route('/trips/new')
def new_trip():
    return render_template("new_trip.html")

@app.route('/create_trip', methods = ["post"])
def create_trip():
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('trip_buddy')
    data = {
    "destination" : request.form["destination"],
    "start" : datetime.datetime.strptime(request.form["startdate"], '%Y-%m-%d'),
    "end" : datetime.datetime.strptime(request.form["enddate"], '%Y-%m-%d'),
    "plan" : request.form["plan"],
    "uid" : session['uid']
    }
    err = []
    if len(data['destination']) < 3:
        err.append("Destination must consist of at least 3 characters")
    if len(data['plan']) < 3:
        err.append("Plan must consist of at least 3 characters")
    if data['start'] < datetime.datetime.now():
        err.append("Start date must be in the future")
    if data['end'] < data['start']:
        err.append("End date must be after the start date")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        query = "INSERT INTO trips (destination, start_date, end_date, plan, created_at, updated_at, created_by) VALUES ( %(destination)s, %(start)s, %(end)s, %(plan)s, NOW(), NOW(), %(uid)s )"
        mysql.query_db(query, data)
        return redirect('/trips')

    return redirect('/trips/new')

@app.route('/delete_trip/<qid>')
def remove_trip(qid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('trip_buddy')
    data = { "q" : int(qid) }
    query = "DELETE FROM trips WHERE trips.id = %(q)s"
    mysql.query_db(query, data)
    return redirect('/trips')

@app.route('/join_trip/<tid>')
def join_trip(tid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('trip_buddy')
    data = { "t" : int(tid), "uid" : session['uid'] }
    query = "INSERT INTO joined_trips (trips_id, users_id) VALUES ( %(t)s, %(uid)s );"
    mysql.query_db(query, data)
    return redirect('/trips')

@app.route('/trips/view/<tripid>')
def users_trips(tripid):
    if not 'uid' in session:
        return redirect('/')
    mysql = connectToMySQL('trip_buddy')
    data = { "tripid" : int(tripid) }
    query = 'SELECT * FROM trips WHERE trips.id = %(tripid)s'
    all_trips = mysql.query_db(query, data)

    mysql = connectToMySQL('trip_buddy')
    query = 'SELECT users.first_name, users.last_name FROM trips JOIN joined_trips ON joined_trips.trips_id = trips.id JOIN users ON users.id = joined_trips.users_id WHERE trips.id = %(tripid)s GROUP BY joined_trips.users_id;'
    people_going = mysql.query_db(query, data)

    return render_template("view_trip.html", trip=all_trips, people=people_going)

@app.route('/trips/edit/<tripid>')
def edit_trip(tripid):
    mysql = connectToMySQL('trip_buddy')
    data = { "id" : int(tripid) }
    query = 'SELECT * FROM trips WHERE id = %(id)s ;'
    trip_data = mysql.query_db(query, data)
    return render_template("edit_trip.html", trip=trip_data)

@app.route('/edit_trip', methods=['post'])
def edit_trip_final():
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('trip_buddy')
    data = {
    "destination" : request.form["destination"],
    "start" : datetime.datetime.strptime(request.form["startdate"], '%Y-%m-%d'),
    "end" : datetime.datetime.strptime(request.form["enddate"], '%Y-%m-%d'),
    "plan" : request.form["plan"],
    "uid" : session['uid']
    }
    err = []
    if len(data['destination']) < 3:
        err.append("Destination must consist of at least 3 characters")
    if len(data['plan']) < 3:
        err.append("Plan must consist of at least 3 characters")
    if data['start'] < datetime.datetime.now():
        err.append("Start date must be in the future")
    if data['end'] < data['start']:
        err.append("End date must be after the start date")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        query = "INSERT INTO trips (destination, start_date, end_date, plan, created_at, updated_at, created_by) VALUES ( %(destination)s, %(start)s, %(end)s, %(plan)s, NOW(), NOW(), %(uid)s )"
        mysql.query_db(query, data)
        return redirect('/trips')

    return redirect('/trips/new')


if __name__ == "__main__":
    app.run(debug=True)
