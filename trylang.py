import time
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 640)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLO model
model = YOLO("best.pt")
print(model.names)

try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Measure inference start time
        start_time = time.time()

        # Run object detection on the frame
        results = model(frame, imgsz=640)

        # Measure inference end time
        end_time = time.time()
        inference_time = end_time - start_time

        # Extract detected object classes
        detected_objects = results[0].boxes.cls.tolist()

        # Print inference time and detected objects
        print(f"Inference Time: {inference_time:.2f} seconds")
        print(f"Detected Objects: {[model.names[int(cls)] for cls in detected_objects]}")

        # Sleep for a short time to prevent excessive looping
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted by the user.")

finally:
    # Clean up resources
    picam2.close()
    print("Resources cleaned up!")