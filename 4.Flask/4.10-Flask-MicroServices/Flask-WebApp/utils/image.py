import cv2
import numpy as np
import base64


def encode_image(image):
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    image_uri = f'data:image/png;base64,{image_base64}'
    return image_uri
