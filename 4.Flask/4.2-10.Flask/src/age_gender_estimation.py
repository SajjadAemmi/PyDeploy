import numpy as np
import cv2
import onnxruntime
from utils import face_align


class AgeGenderEstimator:
    def __init__(self, model_file=None):
        assert model_file is not None
        self.model_file = model_file
        self.input_mean = 0.0
        self.input_std = 1.0
        self.session = onnxruntime.InferenceSession(self.model_file, providers=["CPUExecutionProvider"])
        input_cfg = self.session.get_inputs()[0]
        input_shape = input_cfg.shape
        input_name = input_cfg.name
        self.input_size = tuple(input_shape[2:4][::-1])
        self.input_shape = input_shape
        outputs = self.session.get_outputs()
        output_names = []
        for out in outputs:
            output_names.append(out.name)
        self.input_name = input_name
        self.output_names = output_names
        assert len(self.output_names) == 1

    def __call__(self, img, face):
        bbox = face.bbox
        w, h = (bbox[2] - bbox[0]), (bbox[3] - bbox[1])
        center = (bbox[2] + bbox[0]) / 2, (bbox[3] + bbox[1]) / 2
        rotate = 0
        _scale = self.input_size[0] / (max(w, h) * 1.5)
        aimg, M = face_align.transform(img, center, self.input_size[0], _scale, rotate)
        input_size = tuple(aimg.shape[0:2][::-1])
        blob = cv2.dnn.blobFromImage(
            aimg,
            1.0 / self.input_std,
            input_size,
            (self.input_mean, self.input_mean, self.input_mean),
            swapRB=True,
        )
        pred = self.session.run(self.output_names, {self.input_name: blob})[0][0]
        assert len(pred) == 3
        gender = np.argmax(pred[:2])
        age = int(np.round(pred[2] * 100))
        face["gender"] = gender
        face["age"] = age
        return gender, age
