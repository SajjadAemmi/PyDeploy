import os
import bcrypt
from flask import Flask, jsonify, flash, render_template, request, redirect, url_for, session as flask_session
from sqlmodel import Session, select
from pydantic import BaseModel
from database import get_user_by_username, create_user, engine, User


app = Flask("Analyze Face")
app.secret_key = "my_secret_key"
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}


# PyDantic models for request validation
class RegisterModel(BaseModel):
    city: str
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

def allowed_file(filename):
    return True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        try:
            login_data = LoginModel(
                username=request.form["username"],
                password=request.form["password"]
            )
        except:
            flash("Type error", "warning")
            return redirect(url_for("login"))
        
        user = get_user_by_username(login_data.username)
        if user:
            password_byte = login_data.password.encode("utf-8")
            if bcrypt.checkpw(password_byte, user.password):
                flash("خوش اومدی", "success")
                flask_session["user_id"] = user.id
                return redirect(url_for('profile'))
            else:
                flash("در وارد کردن گذرواژه بیشتر دقت کن", "danger")
                return redirect(url_for("login"))
        else:
            flash("در وارد کردن نام کاربری بیشتر دقت کن", "danger")
            return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        try:
            register_data = RegisterModel(
                city=request.form["city"],
                username=request.form["username"],
                password=request.form["password"])
        except:
            flash("Type error")
            return redirect(url_for("register"))
        
        with Session(engine) as db_session:
            statement = select(User).where(User.username == register_data.username)
            result = db_session.exec(statement).first()
        
        if not result:
            password_byte = register_data.password.encode("utf-8")
            password_hash = bcrypt.hashpw(password_byte, bcrypt.gensalt())
            create_user(register_data.username, password_hash)
            flash("از اینکه در وب‌اپ هوش مصنوعی ثبت نام کردی ازت ممنونم", "success")
            return redirect(url_for("login"))
        else:
            flash("این نام کاربری قبلا استفاده شده دوست من، یک نام کاربری دیگه انتخاب کن", "danger")
            return redirect(url_for("register"))


@app.route("/logout")
def logout():
    flask_session.pop("user_id")
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = flask_session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    with Session(engine) as db_session:
        user = db_session.get(User, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return render_template("profile.html", username=user.username)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if flask_session.get('user_id'):
        if request.method == "GET":
            return render_template("upload.html")
        elif request.method == "POST":
            my_image = request.files['image']
            if my_image.filename == "":
                return redirect(url_for('upload'))
            else:
                if my_image and allowed_file(my_image.filename):
                    save_path = os.path.join(app.config["UPLOAD_FOLDER"], my_image.filename)
                    my_image.save(save_path)
                    result = DeepFace.analyze(
                        img_path = save_path, 
                        actions = ['age'],
                    )
                    age = result[0]['age']

                return render_template("result.html", age=age)
    else:
        return redirect(url_for("index"))
