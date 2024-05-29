from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'hello'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Swaroop@2001'
app.config['MYSQL_DB'] = 'myDb'

app.permanent_session_lifetime = timedelta(days = 15)


db = MySQL(app)

# class users(db.Model):
#     _id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))

#     def __init__(self, id, name, email):
#         self.id = id
#         self.name = name
#         self.email = email


@app.route('/view')
def view():
    cur = db.connection.cursor()
    values=cur.execute('SELECT name FROM users')
    db.connection.commit()
    cur.close()
    
    return render_template('view.html', values=[values])

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True
        id = 2
        user = request.form['name']
        password = request.form['password']
        # email = request.form['email']

        cur = db.connection.cursor()
        cur.execute('INSERT INTO users(id, name, email) VALUES(%s, %s, %s)', (id, user, password))
        db.connection.commit()
        cur.close()
        session['user'] = user
        session['password'] = password

        
        flash('Login Successful', 'info')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already Logged in')
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        password = session['password']
        return render_template('user.html', userdata=[user, password])
    else:
        flash('Please Login!')
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"You've been logged out, {user}", 'info')
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)