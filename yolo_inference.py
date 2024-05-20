from roboflow import Roboflow
import os

roboflow_api_key=os.environ.get("ROBOFLOW_API_KEY")

rf = Roboflow(api_key=roboflow_api_key)
project = rf.workspace().project("dog-breeds-142de")
model = project.version(2).model

result = model.predict("/home/mo/projects/dog_breed_analysis/1280px-003_American_Pit_Bull_Terrier.jpg", confidence=40, overlap=30).json()
result
most_confident_class = result["predictions"][0]["class"].capitalize()
