from roboflow import Roboflow

# Initialize Roboflow with your API key
rf = Roboflow(api_key="ozRCU6q1MWSr8TF2ZLzq")

# Connect to the dataset
project = rf.workspace("universitas-atma-jaya").project("tomato-leaf-disease-rxcft")
version = project.version(6)

# Download it to your D:\tomato folder
print("Starting download...")
dataset = version.download("yolov11")
print("Download complete! Ready for training.")