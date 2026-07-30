# House Price Prediction API 🏠

An end-to-end machine learning pipeline that predicts real estate prices based on user-selected property features.

This project integrates a trained machine learning model with a robust backend API and an interactive web-based frontend, demonstrating a complete deployment workflow.

---

## 🛠️ Tech Stack

- **Machine Learning:** Scikit-Learn (Random Forest Regressor, Pipeline, ColumnTransformer)
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy

---

## ✨ Key Features

- **Interactive UI:** A clean Streamlit interface allowing users to input specific property details.
- **Dynamic Data Serving:** The FastAPI backend serves location data dynamically via a `/locations` endpoint.
- **Smart Schema Handling:** The backend accepts 8 user-selected features and automatically imputes the remaining 14 missing features required by the model pipeline, preventing the need for complete retraining.
- **Production-Ready Routing:** Clear separation of concerns between the prediction model, API logic, and user interface.

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone [https://github.com/RawnaaAbdulfattah/house_price_prediction.git](https://github.com/RawnaaAbdulfattah/house_price_prediction.git)
cd house_price_prediction
```
