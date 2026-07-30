from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import pandas as pd
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="House Price Prediction API")

# Load the model and locations globally when the server starts
model = joblib.load("house_price.pkl")

with open("locations.json", "r") as f:
    locations = json.load(f)

# Define the expected input data structure using Pydantic
class PropertyData(BaseModel):
    area_sqft: float
    bhk: int
    bath: int
    location_grouped: str
    main_road: int
    garden: int
    pool: int
    furnishing_status: str

@app.get("/")
def home():
    return {"message": "House Price Prediction API is running!"}

@app.get("/locations")
def get_locations():
    # Serve the dynamic list to populate frontend dropdowns
    return {"locations": locations}

@app.post("/predict")
def predict_price(data: PropertyData):
    # 1. Map the API inputs back to the original training column names
    # 2. Pad the dropped columns with None so the pipeline's imputer can fill them
    raw_data = {
        # Columns that match exactly
        "area_sqft": data.area_sqft,
        "bhk": data.bhk,
        "location_grouped": data.location_grouped,
        
        # Mapped columns (API name -> Original name)
        "Bathroom": data.bath,
        "Furnishing": data.furnishing_status,
        "overlook_pool": data.pool,
        "overlook_main_road": data.main_road,
        "overlook_garden": data.garden,
        
        # Missing columns padded with None for the SimpleImputer
        "total_floors": None,
        "num_of_parking": None,
        "floor_no": None,
        "facing": None,
        "Transaction": None,
        "Status": None,
        "Ownership": None,
        "parking_type": None,
        "Balcony": None
    }
    
    # 3. Create the DataFrame exactly as the pipeline expects it
    input_df = pd.DataFrame([raw_data])
    
    # 4. Run the prediction
    predicted_log_price = model.predict(input_df)[0]
    
    # 5. Reverse the log transformation
    import numpy as np
    predicted_price = np.expm1(predicted_log_price)
    
    return {"predicted_price": float(predicted_price)}