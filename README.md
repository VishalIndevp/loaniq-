# 💎 LoanIQ — Loan Approval Predictor

> *"It is a prediction, not a spoiler."*

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-84.44%25_Accuracy-00d4a1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 🚀 Live Demo

🔗 **[loaniq.streamlit.app](https://loaniq.streamlit.app)**

---

## 📌 Overview

**LoanIQ** is an AI-powered loan approval prediction web app built with **Streamlit** and **XGBoost**. It takes an applicant's financial and personal profile as input and instantly predicts whether their loan will be **approved or rejected** — along with a confidence score and risk indicators.

The model was trained on real-world applicant data covering Indian states, loan types, employment categories, and financial parameters.

---

## ✨ Features

- ⚡ **Instant predictions** powered by a trained XGBoost classifier
- 🎯 **84.44% model accuracy** on test data
- 📊 **Live summary cards** — Total Income, Debt-to-Income Ratio, Est. EMI
- 🧾 **Applicant profile grid** — full summary of inputs at a glance
- 📈 **Confidence bar** — animated visual showing prediction confidence
- 🚦 **Risk indicators** — DTI Risk, Credit Score flag, Debt Load
- 🌙 **Dark fintech UI** — professional design with hover animations
- 📱 **Mobile responsive** — works on phones, tablets, and desktops
- 🔗 **Social footer** — links to developer profiles

---

## 🖼️ Screenshots

| Sidebar + Dashboard | Prediction Result |
|---|---|
| ![Dashboard](screenshots/dashboard.png) | ![Result](screenshots/result.png) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS |
| **ML Model** | XGBoost Classifier |
| **Preprocessing** | Scikit-learn (StandardScaler) |
| **Data Handling** | Pandas |
| **Serialization** | Joblib |
| **Deployment** | Streamlit Cloud |

---

## 📁 Project Structure

```
loaniq/
│
├── app.py                  # Main Streamlit application
├── model_XGB.pkl           # Trained XGBoost model
├── scaler.pkl              # Fitted StandardScaler
├── model_columns.pkl       # Encoded column names
├── requirements.txt        # Python dependencies
└── README.md               # You are here
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/VishalIndevp/loaniq.git
cd loaniq
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
xgboost
joblib
```

---

## 🧠 Model Details

| Property | Value |
|---|---|
| **Algorithm** | XGBoost Classifier |
| **Accuracy** | 84.44% |
| **Encoding** | One-Hot Encoding (`drop_first=True`) |
| **Scaling** | StandardScaler on numerical features |
| **Features** | 17 input features |

### Input Features

| Feature | Type |
|---|---|
| Gender, Age | Personal |
| Education, Marital Status | Personal |
| Employment Status | Employment |
| Annual Income, Co-Applicant Income | Financial |
| Savings Balance, Existing Loans | Financial |
| State, Property Area | Location |
| Loan Type, Loan Amount, Loan Term | Loan |
| Mortgage, Home Ownership | Property |
| Credit History | Credit |

### Numerical Features (Scaled)

`Age`, `Annual_Income`, `Co_Applicant_Income`, `Savings_Balance`, `Existing_Loans`, `Loan_Amount`, `Loan_Term`

---

## 🌍 Deployment

This app is deployed on **Streamlit Community Cloud**.

To deploy your own version:

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file as `app.py`
5. Click **Deploy**

> ⚠️ Make sure `model_XGB.pkl`, `scaler.pkl`, and `model_columns.pkl` are all committed to the repo.

---

## 📊 How It Works

```
User Input (Sidebar)
        │
        ▼
  Pandas DataFrame
        │
        ▼
One-Hot Encoding (get_dummies)
        │
        ▼
  Column Alignment (reindex)
        │
        ▼
StandardScaler (numerical cols)
        │
        ▼
  XGBoost Predict
        │
        ▼
Approved ✅ / Rejected ❌ + Confidence %
```

---

## 👨‍💻 Developer

**Vishal Singh**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vishal-singh-here/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VishalIndevp)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/vishalindev)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/vishalindev)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a **⭐ star** on GitHub — it means a lot!

---

<div align="center">
  <sub>© 2025 Vishal Singh &nbsp;·&nbsp; 01-03-2026 &nbsp;·&nbsp; LoanIQ · Powered by XGBoost · 84.44% Accuracy</sub>
</div>
