from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://venus_db_809u_user:ENgGqPo9luK6S4cwLchAU9RdpyLMaICM@dpg-conunuf79t8c73bigs90-a.virginia-postgres.render.com/venus_db_809u"
app.config["SECRET_KEY"] = "My SUper Secret Key"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template("index.html", logged_in=False)
    curr_user = User.query.get(session['user_id'])
    return render_template("index.html", logged_in=True, curr_user=curr_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            return redirect('/login')
        
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(password)

            new_user = User(username=username, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('/auth/register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/meeting')
def meeting():
    curr_user = User.query.get(session['user_id'])
    return render_template("meeting.html", curr_user=curr_user)

@app.route('/join', methods=['GET', 'POST'])
def join_meeting():
    if request.method == 'POST':
        meeting_id = request.form.get('room_id')
        return redirect(f'/meeting?roomID={meeting_id}')
    return render_template("join_meeting.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)