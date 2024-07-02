import cv2
from retinaface import RetinaFace
from age_gender import AgeGender


class FaceAnalysis:
    def __init__(self, onnx_model_path):
        # Initialize the face analysis application
        self.face_detection_model = RetinaFace()
        self.face_detection_model.prepare(ctx_id=0, det_size=(640, 640))

        # Load the age and gender model
        self.age_gender_model = AgeGender(onnx_model_path)
        self.age_gender_model.prepare(ctx_id=0)

    def detect_age_gender(self, image):
        faces = self.face_detection_model(image)
        genders = []
        ages = []
        for face in faces:
            bbox = face.bbox.astype(int)
            gender, age = self.age_gender_model.get(image, face)
            genders.append(gender)
            ages.append(age)
            # Draw bounding box and labels on the image
            cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            label = f"Gender: {'Male' if gender == 1 else 'Female'}, Age: {int(age)}"
            cv2.putText(
                image,
                label,
                (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (36, 255, 12),
                2,
            )

        return image, genders, ages


if __name__ == "__main__":
    image_path = "uploads/photo_1403-03-12 18.52.54.jpeg"
    input_image = cv2.imread(image_path)
    if input_image is not None:
        face_analysis = FaceAnalysis("models/genderage.onnx")
        output_image, genders, ages = face_analysis.detect_age_gender(input_image)
        cv2.imshow("Age and Gender Detection", output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Could not read image:", image_path)
