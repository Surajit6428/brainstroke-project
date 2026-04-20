import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template, request, redirect, session,flash
from pymongo import MongoClient
import numpy as np
import pandas as pd
import joblib
import random
import smtplib
import time
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "stroke_secret"


# ================= OTP FUNCTIONS =================

def generate_otp():
    return str(random.randint(100000,999999))


def mask_email(email):

    name, domain = email.split("@")

    if len(name) > 3:
        name = name[:3] + "***"
    else:
        name = name[0] + "***"

    return name + "@" + domain


# ================= EMAIL FUNCTIONS =================

def send_otp_email(receiver_email, otp):

    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    message = MIMEText(f"""
Hello,

Your One-Time Password (OTP) for verification is:{otp}

This OTP is valid for 5 minutes.

Please do not share this code with anyone.

If you did not request this, please ignore this email.

Regards,  
Brain Stroke Prediction Team
""")


    message["Subject"] = "Secure OTP Verification"
    message["From"] = sender_email
    message["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,password)

    server.sendmail(sender_email,receiver_email,message.as_string())
    server.quit()


def send_welcome_email(receiver_email, username, user_password, name):

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")   # ✅ FIX

    message = MIMEText(f"""
Dear {name},

Welcome to the Brain Stroke Prediction System.

Your account has been successfully created. You can now log in and start using our AI-powered prediction service.

----------------------------------------
Account Details:

Username : {username}
Password : {user_password}
----------------------------------------

⚠️ For security reasons, we recommend changing your password after your first login.

If you did not create this account, please ignore this email or contact our support team.

Best regards,  
Brain Stroke Prediction Team  
""")

    message["Subject"] ="🎉 Welcome! Your Brainstroke Account is Ready"
    message["From"] = sender_email
    message["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email, sender_password)   # ✅ FIX

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


# ================= DATABASE =================

client = MongoClient(os.getenv("MONGO_URI"))

db = client["brainstroke_db"]

users = db["users"]
predictions = db["predictions"]

# ================= LOAD MODEL =================

model = joblib.load("stroke_model.pkl")


# ================= HOME =================

@app.route("/")
def home():
   return render_template("index.html")



# ================= SIGNUP =================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        first = request.form.get("first_name")
        middle = request.form.get("middle_name")
        last = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if users.find_one({"username": username}):
            return render_template("signup.html", error="Username already exists", stage="form")

        if users.find_one({"email": email}):
            return render_template("signup.html", error="Email already registered", stage="form")

        otp = generate_otp()

        session["otp"] = otp
        session["otp_time"] = time.time()

        session["temp_user"] = {
            "first_name": first,
            "middle_name": middle,
            "last_name": last,
            "username": username,
            "password": password,
            "email": email
        }

        send_otp_email(email, otp)

        masked = mask_email(email)

        return render_template(
            "signup.html",
            stage="otp",
            email=masked,
            success="OTP sent successfully"
        )

    return render_template("signup.html", stage="form")


# ================= VERIFY SIGNUP OTP =================

@app.route("/verify_otp", methods=["POST"])
def verify_otp():

    user_otp = request.form.get("otp")

    email = session.get("temp_user", {}).get("email")
    masked = mask_email(email) if email else ""

    # OTP expire
    if time.time() - session.get("otp_time", 0) > 300:
        return render_template(
            "signup.html",
            stage="otp",
            email=masked,
            error="OTP expired"
        )

    if user_otp == session.get("otp"):

        user_data = session["temp_user"]

        users.insert_one(user_data)

        send_welcome_email(
            user_data["email"],
            user_data["username"],
            user_data["password"],
            user_data["first_name"]
        )

        session.pop("otp", None)
        session.pop("otp_time", None)
        session.pop("temp_user", None)

        return render_template(
            "signup.html",
            stage="form",
            success="Account created successfully!"
        )

    return render_template(
        "signup.html",
        stage="otp",
        email=masked,
        error="Invalid OTP"
    )


# ================= RESEND SIGNUP OTP =================

@app.route("/resend_otp")
def resend_otp():

    if "temp_user" not in session:
        return redirect("/signup")

    email = session["temp_user"]["email"]

    otp = generate_otp()

    session["otp"] = otp
    session["otp_time"] = time.time()

    send_otp_email(email, otp)

    masked = mask_email(email)

    return render_template(
        "signup.html",
        stage="otp",
        email=masked,
        success="OTP Resent Successfully"
    )

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = users.find_one({"username": username})

        if user and user.get("password") == password:
            session["user"] = username
            flash("Login Successful ✅", "success")
            return redirect("/dashboard")

        flash("Invalid username or password ❌", "error")
        return redirect("/login")

    return render_template("login.html")

# ================= FORGOT PASSWORD (START) =================

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html", stage="email")

# ================= SEND OTP =================
@app.route("/send_reset_otp", methods=["POST"])
def send_reset_otp():

    email = request.form.get("email")

    user = users.find_one({"email": email})

    if not user:
        return render_template(
            "forgot_password.html",
            stage="email",
            error="Email not registered"
        )

    otp = generate_otp()

    session["reset_otp"] = otp
    session["reset_email"] = email
    session["otp_time"] = time.time()

    send_otp_email(email, otp)

    return render_template(
        "forgot_password.html",
        stage="otp",
        email=mask_email(email),
        success="OTP sent successfully"
    )
# ================= VERIFY OTP =================
@app.route("/verify_reset_otp", methods=["POST"])
def verify_reset_otp():

    user_otp = request.form.get("otp")
    email = session.get("reset_email")

    if time.time() - session.get("otp_time",0) > 300:
        return render_template(
            "forgot_password.html",
            stage="otp",
            email=mask_email(email),
            error="OTP expired"
        )

    if user_otp == session.get("reset_otp"):
        return render_template(
            "forgot_password.html",
            stage="new_password",
            success="OTP Verified"
        )

    return render_template(
        "forgot_password.html",
        stage="otp",
        email=mask_email(email),
        error="Wrong OTP"
    )

# ================= RESEND OTP =================
@app.route("/resend_reset_otp")
def resend_reset_otp():

    if "reset_email" not in session:
        return redirect("/forgot_password")

    email = session["reset_email"]

    otp = generate_otp()

    session["reset_otp"] = otp
    session["otp_time"] = time.time()

    send_otp_email(email, otp)

    return render_template(
        "forgot_password.html",
        stage="otp",
        email=mask_email(email),
        success="OTP Resent"
    )


# ================= SET PASSWORD =================
@app.route("/set_new_password", methods=["POST"])
def set_new_password():

    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return render_template(
            "forgot_password.html",
            stage="new_password",
            error="Passwords do not match"
        )

    users.update_one(
        {"email": session["reset_email"]},
        {"$set": {"password": password}}
    )

    session.clear()

    flash("Password updated successfully. Please login.", "success")
    return redirect("/")

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({"username": session["user"]})

    return render_template("dashboard.html",user=user)


# ================= PROFILE =================

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({"username": session["user"]})

    return render_template("profile.html", user=user)

# ================= UPDATE PROFILE =================

@app.route("/update_profile", methods=["POST"])
def update_profile():

    if "user" not in session:
        return redirect("/")

    user = users.find_one({"username": session["user"]})

    first = request.form.get("first_name")
    middle = request.form.get("middle_name")
    last = request.form.get("last_name")
    email = request.form.get("email")

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    message = ""

    # ❌ OLD PASSWORD CHECK
    if old_password:
        if user.get("password") != old_password:
            message = "❌ Incorrect Old Password"
            return render_template("profile.html", user=user, message=message)

    update_data = {
        "first_name": first,
        "middle_name": middle,
        "last_name": last,
        "email": email
    }

    # ✅ PASSWORD UPDATE
    if new_password and new_password.strip() != "":
        update_data["password"] = new_password
        message = "✅ Password Updated Successfully"
    else:
        message = "✅ Profile Updated Successfully"

    users.update_one(
        {"username": session["user"]},
        {"$set": update_data}
    )

    # updated user reload
    user = users.find_one({"username": session["user"]})

    return render_template("profile.html", user=user, message=message)

# ================= HISTORY =================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/")

    data = predictions.find(
        {"user": session["user"]}
    ).sort("_id",-1)

    return render_template("history.html",data=data)


# ================= MANUAL PREDICTION =================

# @app.route("/predict", methods=["POST"])
# def predict():

#     if "user" not in session:
#         return redirect("/")

#     # selected model name from dashboard
#     model_name = request.form.get("model")

#     values = []

#     for x in request.form.getlist("param"):
#         try:
#             values.append(float(x))
#         except:
#             values.append(0)

#     while len(values) < 10:
#         values.append(0)

#     columns = [
#         "gender",
#         "age",
#         "hypertension",
#         "heart_disease",
#         "ever_married",
#         "work_type",
#         "Residence_type",
#         "avg_glucose_level",
#         "bmi",
#         "smoking_status"
#     ]

#     arr = pd.DataFrame([values], columns=columns)

#     pred = model.predict(arr)[0]

#     try:
#         prob = model.predict_proba(arr)[0][1]
#         risk = int(prob * 100)
#     except:
#         risk = 50

#     # store in MongoDB
#     predictions.insert_one({
#         "user": session["user"],
#         "model": model_name,
#         "prediction": int(pred),
#         "risk": risk
#     })

#     return render_template(
#         "result.html",
#         prediction=pred,
#         risk=risk,
#         model=model_name
#     )


# ================= AUTO AI PREDICTION =================

@app.route("/auto_predict", methods=["POST"])
def auto_predict():

    if "user" not in session:
        return redirect("/")

    values = []

    for x in request.form.getlist("param"):
        try:
            values.append(float(x))
        except:
            values.append(0)

    while len(values) < 10:
        values.append(0)

    columns = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "Residence_type",
        "avg_glucose_level",
        "bmi",
        "smoking_status"
    ]

    arr = pd.DataFrame([values], columns=columns)

    pred = model.predict(arr)[0]

    try:
        prob = model.predict_proba(arr)[0][1]
        risk = int(prob * 100)
    except:
        risk = 50

    # 🔥 NEW: Risk Level
    if risk < 30:
        level = "Low"
    elif risk < 70:
        level = "Medium"
    else:
        level = "High"

    predictions.insert_one({
        "user": session["user"],
        "model": "Best Model",
        "prediction": int(pred),
        "risk": risk,
        "level": level   # NEW FIELD
    })

    return render_template(
        "result.html",
        prediction=pred,
        risk=risk,
        level=level,   # SEND TO FRONTEND
        model="Best Model"
    )

# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("user", None)

    # 🔥 clear flash messages
    session.pop('_flashes', None)

    return redirect("/")
# ================= RUN APP =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)