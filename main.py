import requests
import os
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv("api.env")

n_app_id = os.getenv("NUTRITIONX_APP_ID")
n_api_key = os.getenv("NUTRITIONX_API_KEY")
s_api_key = os.getenv("SHEETY_API_KEY")
s_proj_name = os.getenv("SHEETY_PROJECT_NAME")
s_sheet_name = os.getenv("SHEETY_FILE_NAME")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = f"https://api.sheety.co/{s_api_key}/{s_proj_name}/{s_sheet_name}"

question = input("What did you do today: ")

headers = {
    "Content-Type": "application/json",
    "x-app-id": n_app_id,
    "x-app-key": n_api_key,
}

parameters = {
    "query": question,
    "weight_kg": os.getenv("WEIGHT"),
    "height_cm": os.getenv("HEIGHT"),
    "age": os.getenv("AGE"),
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
user_data = response.json()

sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv("BEARER_AUTH")}",
}

for exercise in user_data["exercises"]:
    params_to_post = {
        "workout": {
            "date": f"{dt.now().strftime('%d/%m/%Y')}",
            "time": f"{dt.now().strftime('%H:%M:%S')}",
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheety_requests = requests.post(url=sheety_endpoint, json=params_to_post, headers=sheety_headers)

    print(sheety_requests.text)
