<h1 align="center">🧠 Brain Stroke Prediction System</h1>

<p align="center">
🚀 AI-powered web application to predict stroke risk using Machine Learning  
</p>

<p align="center">
Flask • MongoDB • Scikit-learn
</p>

---

## 📌 Introduction

The **Brain Stroke Prediction System** is a full-stack web application that predicts the probability of a stroke based on user health data.

It helps in **early detection**, reducing serious health risks using AI.

---

## 🎯 Features

### 🔐 Authentication
- Signup with Email OTP verification
- Login system
- Forgot Password (OTP reset)

### 🧠 Prediction System
- AI-based stroke prediction
- Risk percentage (%)
- Risk levels:
  - 🟢 Low
  - 🟡 Medium
  - 🔴 High

### 👤 User Features
- Profile management
- Update details & password
- Prediction history tracking

### 🎨 UI Features
- Responsive design
- Dark / Light mode
- Animated UI
- Modern dashboard

---

## 🧠 Machine Learning

- Dataset: `Brain.csv`
- Data size: 50,000 samples

### Models Used:
- Logistic Regression
- Decision Tree
- Random Forest ✅ (Best Model)

### Output:
- Stroke Risk (%)
- Risk Level (Low / Medium / High)

---

## ⚙️ Tech Stack

### 💻 Frontend
- HTML
- CSS
- JavaScript

### 🔧 Backend
- Flask (Python)

### 🗄 Database
- MongoDB Atlas

### 🤖 ML Libraries
- Pandas
- NumPy
- Scikit-learn
- Joblib

---

## 📁 Project Structure


## 📁 Project Structure

<pre>

BRAINSTROKE/
│
├── static/
│   ├── bg.jpg
│   ├── favicon.png
│   ├── logo.png
│   └── stroke.png
│
├── templates/
│   ├── dashboard.html
│   ├── forgot_password.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── result.html
│   └── signup.html
│
├── __pycache__/
│
├── app.py
├── train_model.py
├── stroke_model.pkl
├── Brain.csv
│
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── (Flask Run Entry)
</pre>


---

## 🔧 Installation & Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt

SECRET_KEY=your_secret_key

MONGO_URI=your_mongodb_uri

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

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

