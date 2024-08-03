import argparse
import yaml
import cv2
import numpy as np
import onnxruntime as ort


class YOLOv8:
    def __init__(self, onnx_model_path, confidence_threshold=0.5, iou_threshold=0.5):
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        with open("coco8.yaml") as stream:
            self.classes = yaml.safe_load(stream)["names"]
        self.session = ort.InferenceSession(
            onnx_model_path, providers=["CPUExecutionProvider"]
        )
        self.model_inputs = self.session.get_inputs()
        self.input_width, self.input_height = self.model_inputs[0].shape[2:4]

    def draw_detections(self, image, box, score, class_id):
        x1, y1, w, h = box
        color = (0, 255, 0)
        cv2.rectangle(image, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        label = f"{self.classes[class_id]}: {score:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(
            image,
            (label_x, label_y - label_height),
            (label_x + label_width, label_y + label_height),
            color,
            cv2.FILLED,
        )
        cv2.putText(
            image,
            label,
            (label_x, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

    def preprocess(self, image):
        self.image_height, self.image_width = image.shape[:2]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.input_width, self.input_height))
        image_data = np.array(image, dtype=np.float32) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))  # Channel first
        image_data = np.expand_dims(image_data, axis=0)
        return image_data

    def postprocess(self, input_image, output):
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes = []
        scores = []
        class_ids = []
        x_factor = self.image_width / self.input_width
        y_factor = self.image_height / self.input_height

        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            if max_score >= self.confidence_threshold:
                class_id = np.argmax(classes_scores)
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        indices = cv2.dnn.NMSBoxes(
            boxes, scores, self.confidence_threshold, self.iou_threshold
        )

        output_boxes = np.array(boxes)[indices]
        output_scores = np.array(scores)[indices]
        output_class_ids = np.array(class_ids)[indices]
        output_labels = []
        for output_class_id in output_class_ids:
            output_labels.append(self.classes[output_class_id])
        output_image = input_image.copy()
        for i in indices:
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            self.draw_detections(output_image, box, score, class_id)
        return output_image, output_labels

    def __call__(self, input_image):
        image_data = self.preprocess(input_image)
        outputs = self.session.run(None, {self.model_inputs[0].name: image_data})
        output_image, output_labels = self.postprocess(input_image, outputs)
        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        return output_image, output_labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image", type=str, required=True ,help="Input image path",
    )
    parser.add_argument(
        "--model", type=str, default="models/yolov8n.onnx", help="ONNX model path"
    )
    parser.add_argument(
        "--conf-threshold", type=float, default=0.5, help="Confidence threshold"
    )
    parser.add_argument(
        "--iou-threshold", type=float, default=0.5, help="NMS IoU threshold"
    )
    args = parser.parse_args()

    object_detector = YOLOv8(args.model, args.conf_threshold, args.iou_threshold)
    input_image = cv2.imread(args.image)
    output_image, output_labels = object_detector(input_image)

    print(output_labels)

    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    cv2.imshow("Output", output_image)
    cv2.waitKey(0)
