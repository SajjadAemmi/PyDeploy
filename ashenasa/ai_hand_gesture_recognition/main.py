# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from visualization import display_batch_of_images_with_gestures_and_hand_landmarks


# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path="gesture_recognizer.task")
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

IMAGE_FILENAMES = [
    "assets/thumbs_down.jpg",
    "assets/victory.jpg",
    "assets/thumbs_up.jpg",
    "assets/pointing_up.jpg",
]

images = []
results = []
for image_file_name in IMAGE_FILENAMES:
    # STEP 3: Load the input image.
    image = mp.Image.create_from_file(image_file_name)

    # STEP 4: Recognize gestures in the input image.
    recognition_result = recognizer.recognize(image)

    # STEP 5: Process the result. In this case, visualize it.
    images.append(image)
    top_gesture = recognition_result.gestures[0][0]
    hand_landmarks = recognition_result.hand_landmarks
    results.append((
        top_gesture, 
        # hand_landmarks
        ))

print(results)

# display_batch_of_images_with_gestures_and_hand_landmarks(images, results)
