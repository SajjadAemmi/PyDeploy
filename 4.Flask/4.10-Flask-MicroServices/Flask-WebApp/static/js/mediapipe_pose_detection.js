// Copyright 2023 The MediaPipe Authors.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
import { PoseLandmarker, FilesetResolver, DrawingUtils } from "https://cdn.skypack.dev/@mediapipe/tasks-vision@0.10.0";
const demosSection = document.getElementById("demos");
let poseLandmarker = undefined;
let runningMode = "IMAGE";
let enableWebcamButton;
let webcamRunning = false;
const videoHeight = "360px";
const videoWidth = "480px";
// Before we can use PoseLandmarker class we must wait for it to finish
// loading. Machine Learning models can be large and take a moment to
// get everything needed to run.
const createPoseLandmarker = async () => {
    const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm");
    poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
            delegate: "GPU"
        },
        runningMode: runningMode,
        numPoses: 2
    });
    demosSection.classList.remove("invisible");
};
createPoseLandmarker();
/********************************************************************
// Demo 1: Grab a bunch of images from the page and detection them
// upon click.
********************************************************************/
// In this demo, we have put all our clickable images in divs with the
// CSS class 'detectionOnClick'. Lets get all the elements that have
// this class.
const imageContainers = document.getElementsByClassName("detectOnClick");
// Now let's go through all of these and add a click event listener.
for (let i = 0; i < imageContainers.length; i++) {
    // Add event listener to the child element whichis the img element.
    imageContainers[i].children[0].addEventListener("click", handleClick);
}
// When an image is clicked, let's detect it and display results!
async function handleClick(event) {
    if (!poseLandmarker) {
        console.log("Wait for poseLandmarker to load before clicking!");
        return;
    }
    if (runningMode === "VIDEO") {
        runningMode = "IMAGE";
        await poseLandmarker.setOptions({ runningMode: "IMAGE" });
    }
    // Remove all landmarks drawed before
    const allCanvas = event.target.parentNode.getElementsByClassName("canvas");
    for (var i = allCanvas.length - 1; i >= 0; i--) {
        const n = allCanvas[i];
        n.parentNode.removeChild(n);
    }
    // We can call poseLandmarker.detect as many times as we like with
    // different image data each time. The result is returned in a callback.
    poseLandmarker.detect(event.target, (result) => {
        const canvas = document.createElement("canvas");
        canvas.setAttribute("class", "canvas");
        canvas.setAttribute("width", event.target.naturalWidth + "px");
        canvas.setAttribute("height", event.target.naturalHeight + "px");
        canvas.style =
            "left: 0px;" +
                "top: 0px;" +
                "width: " +
                event.target.width +
                "px;" +
                "height: " +
                event.target.height +
                "px;";
        event.target.parentNode.appendChild(canvas);
        const canvasCtx = canvas.getContext("2d");
        const drawingUtils = new DrawingUtils(canvasCtx);
        for (const landmark of result.landmarks) {
            drawingUtils.drawLandmarks(landmark, {
                radius: (data) => DrawingUtils.lerp(data.from.z, -0.15, 0.1, 5, 1)
            });
            drawingUtils.drawConnectors(landmark, PoseLandmarker.POSE_CONNECTIONS);
        }
    });
}
/********************************************************************
// Demo 2: Continuously grab image from webcam stream and detect it.
********************************************************************/
const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");
const drawingUtils = new DrawingUtils(canvasCtx);
// Check if webcam access is supported.
const hasGetUserMedia = () => { var _a; return !!((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia); };
// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
    enableWebcamButton = document.getElementById("webcamButton");
    enableWebcamButton.addEventListener("click", enableCam);
}
else {
    console.warn("getUserMedia() is not supported by your browser");
}
// Enable the live webcam view and start detection.
function enableCam(event) {
    if (!poseLandmarker) {
        console.log("Wait! poseLandmaker not loaded yet.");
        return;
    }
    if (webcamRunning === true) {
        webcamRunning = false;
        enableWebcamButton.innerText = "ENABLE PREDICTIONS";
    }
    else {
        webcamRunning = true;
        enableWebcamButton.innerText = "DISABLE PREDICTIONS";
    }
    // getUsermedia parameters.
    const constraints = {
        video: true
    };
    // Activate the webcam stream.
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
}
let lastVideoTime = -1;
async function predictWebcam() {
    canvasElement.style.height = videoHeight;
    video.style.height = videoHeight;
    canvasElement.style.width = videoWidth;
    video.style.width = videoWidth;
    // Now let's start detecting the stream.
    if (runningMode === "IMAGE") {
        runningMode = "VIDEO";
        await poseLandmarker.setOptions({ runningMode: "VIDEO" });
    }
    let startTimeMs = performance.now();
    if (lastVideoTime !== video.currentTime) {
        lastVideoTime = video.currentTime;
        poseLandmarker.detectForVideo(video, startTimeMs, (result) => {
            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            for (const landmark of result.landmarks) {
                drawingUtils.drawLandmarks(landmark, {
                    radius: (data) => DrawingUtils.lerp(data.from.z, -0.15, 0.1, 5, 1)
                });
                drawingUtils.drawConnectors(landmark, PoseLandmarker.POSE_CONNECTIONS);
            }
            canvasCtx.restore();
        });
    }
    // Call this function again to keep predicting when the browser is ready.
    if (webcamRunning === true) {
        window.requestAnimationFrame(predictWebcam);
    }
}