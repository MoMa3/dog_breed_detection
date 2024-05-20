from roboflow import Roboflow
import os
from dotenv import load_dotenv
from pathlib import Path 
load_dotenv(Path(".env"))
roboflow_api_key=os.environ.get("ROBOFLOW_API_KEY")

rf = Roboflow(api_key=roboflow_api_key)
project = rf.workspace().project("dog-breeds-142de")
model = project.version(2).model


def get_most_confident_prediction(img_path):
    result = model.predict(img_path, confidence=40, overlap=30).json()
    most_confident_class = result["predictions"][0]["class"].capitalize()
    return most_confident_class
