# 🧠 Brain Stroke Prediction Web App

A full-stack Machine Learning web application that predicts the risk of brain stroke based on user health data.
Built using **Flask, MongoDB, and Scikit-learn**.

---

## 🚀 Features

* 🔐 User Authentication (Signup, Login, OTP Verification)
* 📧 Email-based OTP system
* 🧠 Stroke Prediction using trained ML model
* 📊 Dashboard with prediction history
* 👤 User Profile Management
* 🔁 Forgot Password & Reset System
* 💾 MongoDB database integration

---

## 🛠️ Technologies Used

* **Frontend:** HTML
* **Backend:** Flask (Python)
* **Database:** MongoDB
* **Machine Learning:** Scikit-learn
* **Libraries:** NumPy, Pandas, Joblib

---

## 📁 Project Structure

<pre>

BRAINSTROKE/
│
├── templates/
│   ├── dashboard.html
│   ├── forgot_password.html
│   ├── history.html
│   ├── login.html
│   ├── login_error.html
│   ├── new_password.html
│   ├── profile.html
│   ├── reset_verify.html
│   ├── result.html
│   ├── signup.html
│   ├── signup_success.html
│   ├── user_exists.html
│   ├── verify_otp.html
│
├── model/
│   └── stroke_model.pkl
│
├── dataset/
│   └── stroke_dataset_500k_balanced.csv
│
├── app.py
├── train_model.py
├── requirements.txt
├── .env
├── README.md
</pre>
---

## 📦 Installation & Setup

### 1️⃣ Install Dependencies

pip install -r requirements.txt

---

### 2️⃣ Start MongoDB

Make sure MongoDB is installed and running:

mongod

---

### 3️⃣ Add Dataset

Place the dataset file inside the project folder:

stroke_dataset_500k_balanced.csv

---

### 4️⃣ Train the Model (Optional)

python train_model.py

This will generate:

stroke_model.pkl

---

### 5️⃣ Run the Application

python app.py

---

### 6️⃣ Open in Browser

http://127.0.0.1:5000

---

## 🔑 Environment Variables (.env)

Create a `.env` file and add:

SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/brainstroke
EMAIL_USER=[your_email@gmail.com](mailto:your_email@gmail.com)
EMAIL_PASS=your_email_password

---

## 🧠 Machine Learning Model

* Dataset: Stroke Dataset (500k balanced)
* Algorithms: Logistic Regression / Random Forest
* Output: Stroke Risk (Yes / No)

---

## ⚠️ Important Notes

* MongoDB must be running before starting the app
* Email credentials are required for OTP verification
* Ensure `stroke_model.pkl` exists before running app
* Update file paths if you change folder structure

---

## 👨‍💻 Author

**Surajit Bhowmik**
**Prabir Barik**
**Ayan Dogra**
**Ranit Kar**
**Asanur Baidya**
**Guide By Mr.Partha Sankar Nayek**

---

## ⭐ Future Improvements

* 📱 Responsive UI design
* ☁️ Cloud deployment (Render / AWS)
* 🤖 AI chatbot integration
* 📊 Advanced analytics dashboard

---

## ❤️ Thank You
