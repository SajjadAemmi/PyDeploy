# from deepface import DeepFace

# result = DeepFace.verify(
#   img1_path = "uploads/photo_1403-03-12 18.52.42.jpeg",
#   img2_path = "uploads/photo_1403-03-12 18.52.42.jpeg",
# )

# face_objs = DeepFace.extract_faces(
#   img_path = "uploads/photo_1403-03-12 18.52.42.jpeg",
# )
# print(face_objs)

# objs = DeepFace.analyze(
#   img_path = "uploads/photo_1403-03-12 18.52.42.jpeg",
#   actions = ['age' 
#             #  'gender', 'race', 'emotion'
#             ]
# )

# print(objs[0]['age'])

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n-cls.pt")  # load a pretrained model (recommended for training)

results = model("uploads/Firefly - The magical lion.jpg")  # predict on an image
for result in results:
  print(result.names[result.probs.top1])
