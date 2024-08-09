# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import os

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",  # React's default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="LicensePlates"), name="static")

class StateResponse(BaseModel):
    state: str

@app.get("/api/state", response_model=StateResponse)
async def get_random_state():
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
              "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
              "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
              "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
              "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
              "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
              "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
              "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin",
              "Wyoming"]
    state = random.choice(states)
    return {"state": state}

@app.get("/api/license_plates")
async def get_license_plates():
    plates = [f"/static/{file}" for file in os.listdir("LicensePlates")]
    return {"license_plates": plates}

@app.get("/api/license_plates/{state}")
async def get_license_plate(state: str):
    license_plate_path = f"LicensePlates/{state}.png"  # Change to .png
    if not os.path.exists(license_plate_path):
        raise HTTPException(status_code=404, detail="License plate not found")
    return {"license_plate_path": license_plate_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
