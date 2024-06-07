from flask import Flask, request, jsonify, session as flask_session, render_template, redirect, url_for
from sqlmodel import Field, SQLModel, create_engine, Session, select
import bcrypt
from pydantic import BaseModel


app = Flask(__name__)
app.secret_key = 'supersecretkey'


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
SQLModel.metadata.create_all(engine)

# Pydantic models for request validation
class RegisterModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

# Helper functions
def get_user_by_username(username: str):
    with Session(engine) as db_session:
        statement = select(User).where(User.username == username)
        return db_session.exec(statement).first()

def create_user(username: str, password: str):
    password_bytes = password.encode('utf-8')
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    user = User(username=username, password_hash=password_hash)
    with Session(engine) as db_session:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, password_hash)

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        try:
            register_data = RegisterModel(username=data['username'], password=data['password'])
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        if get_user_by_username(register_data.username):
            return jsonify({'error': 'Username already exists'}), 400

        user = create_user(register_data.username, register_data.password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        try:
            login_data = LoginModel(username=data['username'], password=data['password'])
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        user = get_user_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 400

        flask_session['user_id'] = user.id
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    flask_session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET'])
def profile():
    user_id = flask_session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    with Session(engine) as db_session:
        user = db_session.get(User, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

    return render_template('profile.html', username=user.username)

if __name__ == '__main__':
    app.run(debug=True)
