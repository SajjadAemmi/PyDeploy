import os
from flask import Flask, render_template, request, redirect, url_for, session
from deepface import DeepFace
import cv2


app = Flask("Analyze Face")
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}


def auth(email, password):
    if email == "sajjad@sajjad.sajjad" and password == "1234":
        return True
    else:
        return False


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
        my_email = request.form["email"]
        my_password = request.form["password"]
        result = auth(my_email, my_password)
        if result:
            return redirect(url_for('upload'))
        else:
            return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
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
