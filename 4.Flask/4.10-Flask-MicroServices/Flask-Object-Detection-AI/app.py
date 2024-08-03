from flask import Flask, request, jsonify, send_file
import numpy as np
import io
import base64
from PIL import Image
from src.object_detection import YOLOv8


app = Flask(__name__)

object_detector = YOLOv8("models/yolov8n.onnx")


# def object_detector(input_image):
#     # Your object detection logic here
#     # This is a placeholder implementation
#     output_image = input_image  # Processed image
#     labels = ["label1", "label2"]  # Detected object labels
#     return output_image, labels


@app.route("/detect", methods=["POST"])
def detect_objects():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file.stream)
        input_image = np.array(image)

        output_image, labels = object_detector(input_image)

        # output_image_pil = Image.fromarray(output_image)
        # byte_arr = io.BytesIO()
        # output_image_pil.save(byte_arr, format="PNG")
        # byte_arr.seek(0)
        # encoded_img = base64.b64encode(byte_arr.read()).decode("utf-8")

        response = {
            # "output_image": encoded_img, 
            "labels": labels
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
