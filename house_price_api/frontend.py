import streamlit as st
import requests

# Define the backend API URLs
API_URL = "http://127.0.0.1:8000"

st.title("🏡 Real Estate Price Predictor")
st.write("Enter the property details below to get an instant price estimate.")

# Fetch the locations from the FastAPI backend securely
import requests
import streamlit as st

@st.cache_data
def get_locations():
    try:
        response = requests.get("http://127.0.0.1:8000/locations")
        if response.status_code == 200:
            data = response.json()
            
            # --- THE FIX ---
            # If the API returns a dictionary like {"locations": [...]}, extract the list
            if isinstance(data, dict) and "locations" in data:
                return data["locations"]
            
            # If it's already a list, just return it
            return data
        else:
            return []
    except Exception as e:
        return []

# Then use it for your dropdown:
# locations = get_locations()
# selected_location = st.selectbox("Location", locations)

locations = get_locations()

# Create the user interface layout
st.header("Property Details")

# Group inputs into columns for a cleaner UI
col1, col2 = st.columns(2)

with col1:
    area_sqft = st.number_input("Area (Square Feet)", min_value=300, max_value=10000, value=1200, step=100)
    bhk = st.number_input("Bedrooms (BHK)", min_value=1, max_value=10, value=3)
    bath = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
    location_grouped = st.selectbox("Location", locations)

with col2:
    furnishing_status = st.selectbox("Furnishing Status", ["Unfurnished", "Semi-Furnished", "Furnished"])
    main_road = st.checkbox("Facing Main Road")
    garden = st.checkbox("Has Garden")
    pool = st.checkbox("Has Pool")

# Prediction button
if st.button("Predict Price", type="primary"):
    # Map the UI inputs to the exact JSON structure your FastAPI expects
    payload = {
        "area_sqft": area_sqft,
        "bhk": bhk,
        "bath": bath,
        "location_grouped": location_grouped,
        "main_road": 1 if main_road else 0,
        "garden": 1 if garden else 0,
        "pool": 1 if pool else 0,
        "furnishing_status": furnishing_status
    }
    
    # Send the POST request to the backend
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        response.raise_for_status()
        
        # Extract the prediction and display it
        prediction = response.json()["predicted_price"]
        
        st.success("Prediction Complete!")
        st.metric(label="Estimated Property Value", value=f"₹ {prediction:,.2f}")
        
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the prediction server. Is FastAPI running? Error: {e}")