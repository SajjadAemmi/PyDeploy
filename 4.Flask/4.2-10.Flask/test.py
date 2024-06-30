from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

path = model.export(format="onnx")  # export the model to ONNX format