import os
import bcrypt
import cv2
import numpy as np
import base64
from PIL import Image
from flask import Flask, jsonify, send_file, flash, render_template, request, redirect, url_for, session as flask_session
from sqlmodel import Session, select
from database import get_user_by_username, create_user, engine, User, Comment
from models import LoginModel, RegisterModel
from src.face_analysis import FaceAnalysis
from src.object_detection import YOLOv8
from utils.image import encode_image


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask("AI Web App")
app.secret_key = "my_secret_key"
app.config["UPLOAD_FOLDER"] = './uploads'

face_analysis = FaceAnalysis("models/det_10g.onnx", "models/genderage.onnx")
object_detector = YOLOv8("models/yolov8n.onnx")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            if bcrypt.checkpw(password_byte, bytes(user.password, "utf-8")):
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
            password_hash = password_hash.decode('utf8')
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


@app.route("/ai-face-analysis", methods=["GET", "POST"])
def ai_face_analysis():
    if flask_session.get('user_id'):
        if request.method == "GET":
            return render_template("ai_face_analysis.html")
        elif request.method == "POST":
            input_image_file = request.files['image']
            if input_image_file.filename == "":
                return redirect(url_for('upload'))
            else:
                if input_image_file and allowed_file(input_image_file.filename):
                    input_image = Image.open(input_image_file.stream)
                    input_image = np.array(input_image)
                    output_image, genders, ages = face_analysis.detect_age_gender(input_image)
                    image_uri = encode_image(output_image)
                    return render_template("ai_face_analysis.html", genders=genders, ages=ages, image_uri=image_uri)
    else:
        return redirect(url_for("index"))


@app.route("/ai-object-detection", methods=["GET", "POST"])
def ai_object_detection():
    if flask_session.get('user_id'):
        if request.method == "GET":
            return render_template("ai_object_detection.html")
        elif request.method == "POST":
            input_image_file = request.files['image']
            if input_image_file.filename == "":
                return redirect(url_for('upload'))
            else:
                if input_image_file and allowed_file(input_image_file.filename):
                    input_image = Image.open(input_image_file.stream)
                    input_image = np.array(input_image)
                    output_image, labels = object_detector(input_image)
                    image_uri = encode_image(output_image)
                    return render_template("ai_object_detection.html", labels=labels, image_uri=image_uri)
    else:
        return redirect(url_for("index"))


@app.route("/ai-pose-detection", methods=["GET"])
def ai_pose_detection():
    if flask_session.get('user_id'):
        return render_template("ai_pose_detection.html")
    else:
        return redirect(url_for("index"))


@app.route('/mind-reader')
def mind_reader():
    return render_template('mind_reader.html')

@app.route('/mind-reader-process', methods=['POST'])
def mind_reader_process():
    x = request.form['number']
    return redirect(url_for('mind_reader_result', number=x))

@app.route('/mind-reader-result')
def mind_reader_result():
    number = request.args.get('number')
    return render_template('mind_reader_result.html', number=number)


@app.route('/create-new-comment')
def create_new_comment():
    with Session(engine) as db_session:
        new_comment = Comment(user_id=1, content="This is a user comment.")
        db_session.add(new_comment)
        db_session.commit()
