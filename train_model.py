import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC

from sklearn.metrics import accuracy_score


# ================= LOAD DATA =================

data = pd.read_csv("stroke_dataset_500k_balanced.csv")

print("Original Dataset Size:", len(data))


# ================= SAMPLING =================

data = data.sample(50000, random_state=42)

print("Training Dataset Size:", len(data))


# ================= ENCODE CATEGORICAL DATA =================

for col in data.select_dtypes(include=["object","string"]):

    le = LabelEncoder()

    data[col] = le.fit_transform(data[col])

print("Categorical Encoding Completed")


# ================= SPLIT FEATURES & TARGET =================

X = data.drop(["stroke","id"], axis=1)

y = data["stroke"]


# ================= TRAIN TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Train Test Split Completed")


# ================= MODELS =================

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=500),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(n_estimators=100, random_state=42),

    # "Support Vector Machine":
    #     SVC(kernel="linear", probability=True)

}


# ================= TRAIN MODELS =================

best_model = None
best_accuracy = 0
best_model_name = ""

print("\nTraining Models...\n")


for name, model in models.items():

    print("Training:", name)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", round(accuracy * 100, 2), "%\n")


    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name


# ================= BEST MODEL =================

print("Best Model:", best_model_name)

print("Best Accuracy:", round(best_accuracy * 100, 2), "%")


# ================= SAVE MODEL =================

joblib.dump(best_model, "stroke_model.pkl")

print("\nBest Model Saved Successfully")