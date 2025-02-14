document.addEventListener("DOMContentLoaded", function () {
    let video = document.getElementById("video");
    let canvas = document.getElementById("canvas");
    let captureBtn = document.getElementById("capture-btn");
    let capturedImageField = document.getElementById("captured_image");
    
    let uploadOption = document.getElementById("upload-option");
    let captureOption = document.getElementById("capture-option");
    let manualOption = document.getElementById("manual-option");

    let uploadContainer = document.getElementById("upload-container");
    let cameraContainer = document.getElementById("camera-container");
    let manualContainer = document.getElementById("manual-container");

    let scanBtn = document.getElementById("scan-btn");
    let stream = null;  // Store the webcam stream

    // Toggle between Upload, Capture, or Manual options
    function toggleInputs() {
        uploadContainer.style.display = uploadOption.checked ? "block" : "none";
        cameraContainer.style.display = captureOption.checked ? "block" : "none";
        manualContainer.style.display = manualOption.checked ? "block" : "none";

        if (captureOption.checked) {
            startWebcam();
        } else {
            stopWebcam();
        }
    }

    uploadOption.addEventListener("change", toggleInputs);
    captureOption.addEventListener("change", toggleInputs);
    manualOption.addEventListener("change", toggleInputs);

    function startWebcam() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (mediaStream) {
                stream = mediaStream;
                video.srcObject = mediaStream;
            })
            .catch(function (err) {
                console.error("Error accessing webcam:", err);
                alert("Webcam access denied or unavailable.");
            });
    }

    function stopWebcam() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }

    // Capture image from video stream
    captureBtn.addEventListener("click", function () {
        let context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        let imageData = canvas.toDataURL("image/png");  // Convert to base64
        capturedImageField.value = imageData;  // Store in hidden input

        alert("Photo captured! Click 'Proceed' to continue.");
    });

    // Ensure at least one option is selected before scanning
    scanBtn.addEventListener("click", function (event) {
        if (!uploadOption.checked && !captureOption.checked && !manualOption.checked) {
            alert("Please select one method (Upload, Capture, or Manual Entry).");
            event.preventDefault();  // Prevent form submission
        }
    });

    // Ensure webcam stops when user leaves the page
    window.addEventListener("beforeunload", stopWebcam);
});
