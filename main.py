from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel

app = FastAPI()

# GET request
@app.get("/")
def read_root():
    return {"message": " Football api"}

# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

model = joblib.load('Models/knn_model.joblib')
scaler = joblib.load('Models/scaler.joblib')



class InputFeatures(BaseModel):
      appearance: int
      goals: float
      minutes_played: int 
      games_injured: int
      highest_value: int







def preprocessing(input_features: InputFeatures):
    dict_f = {
        'appearance': input_features.appearance,
        'goals': input_features.goals,
        
        'minutes_played': input_features.minutes_played,
        
        'games_injured': input_features.games_injured,

        'highest_value': input_features.highest_value,
   
    }

    # Convert dictionary values to a list in the correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]
    # Scale the input features
    scaled_features = scaler.transform([features_list])
    return scaled_features

@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    y_pred = model.predict(data)
    return {"pred": y_pred.tolist()[0]}


