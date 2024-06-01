from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel

app = FastAPI()

# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to Football api"}

# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

model = joblib.load('Models/knn_model.joblib')
scaler = joblib.load('Models/scaler.joblib')

# Define a Pydantic model for input data validation

class InputFeatures(BaseModel):
    league: str
    appearance: int
    goals: float
    assists: float
    minutes_played: int 
    days_injured: int
    games_injured: int
    award: int
    highest_value: int


#appearance	goals	assists	minutes played	days_injured	games_injured	award
#highest_value	league_DStv	league_K-League	league_La liga	league_Premier League and Championship	league_Serie A
#appearance	goals	assists	minutes played	days_injured	games_injured	award	highest_value	league_DStv	league_K-League	league_La liga	league_Premier League and Championship	league_Serie A
def preprocessing(input_features: InputFeatures):
    dict_f = {
        'appearance': input_features.appearance,
        'goals': input_features.goals,
        'assists': input_features.assists,
        'minutes_played': input_features.minutes_played,
        'days_injured': input_features.days_injured,
        'games_injured': input_features.games_injured,
        'award': input_features.award,
        'highest_value': input_features.highest_value,
        'league_DStv': input_features.league == 'league_DStv',
        'league_La liga': input_features.league == 'league_La liga',
        'league_K-League': input_features.league == 'league_K-League',
        'league_Premier League and Championship': input_features.league == 'league_Premier League and Championship',
        'league_Serie A': input_features.league == 'league_Serie A',
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


