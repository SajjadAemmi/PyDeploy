import onnxruntime as ort
import cv2
import numpy as np

# Load the ONNX model
model_path = 'yolov8n.onnx'
session = ort.InferenceSession(model_path)

# Load the image
image_path = 'uploads/Firefly - The magical lion.jpg'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_height, image_width = image.shape[:2]

# Preprocess the image: resize, normalize and add batch dimension
input_size = (640, 640)  # This size should match the model's expected input size
input_image = cv2.resize(image, input_size)
input_image = input_image / 255.0
input_image = np.transpose(input_image, (2, 0, 1))  # Change data layout from HWC to CHW
input_image = np.expand_dims(input_image, axis=0)  # Add batch dimension
input_image = input_image.astype(np.float32)

# Get input name for the ONNX model
input_name = session.get_inputs()[0].name

# Perform inference
outputs = session.run(None, {input_name: input_image})

outputs = np.transpose(np.squeeze(outputs[0]))


# Post-processing
# Assuming the model output is in the format [batch, num_boxes, box_params]
# where box_params include [x_center, y_center, width, height, objectness, class_scores...]

boxes = outputs[:, :4]
scores = outputs[:, 4]
class_scores = outputs[:, 5:]

# Filter out boxes with low confidence
confidence_threshold = 0.1
boxes = boxes[scores > confidence_threshold]
class_scores = class_scores[scores > confidence_threshold]
scores = scores[scores > confidence_threshold]

# Convert boxes from [x_center, y_center, width, height] to [x1, y1, x2, y2]
# boxes[:, 0] = boxes[:, 0] - (boxes[:, 2] / 2)
# boxes[:, 1] = boxes[:, 1] - (boxes[:, 3] / 2)
# boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
# boxes[:, 3] = boxes[:, 1] + boxes[:, 3]

print(boxes)

# Scale boxes back to original image size
boxes[:, [0, 2]] *= image_width / input_size[0]
boxes[:, [1, 3]] *= image_height / input_size[1]

print(boxes)


# Draw the boxes on the image
for box, score in zip(boxes, scores):
    x1, y1, x2, y2 = box.astype(int)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, f'{score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save the resulting image
result_image_path = 'result.jpg'
cv2.imwrite(result_image_path, image)
