from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO("axon_model_20250512.pt")

# Export the model
model.export(format="openvino", imgsz=1024)  # creates 'yolov8n_openvino_model/'

#REFERENCE: https://docs.ultralytics.com/integrations/openvino/#how-do-i-export-yolov8-models-to-openvino-format
