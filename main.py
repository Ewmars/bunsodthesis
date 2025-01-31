import cv2
from ultralytics import YOLO
import argparse
import sys


def parse_arguments():
    # Check if running in Jupyter
    if "ipykernel_launcher" in sys.argv[0]:
        # Provide default arguments for Jupyter
        return argparse.Namespace(webcam_resolution=[1280, 720])
    
    # Otherwise, parse command-line arguments
    parser = argparse.ArgumentParser(description="YOLOV8 Live Camera Stream")
    parser.add_argument("--webcam-resolution", type=int, default=[1280, 720], nargs=2, help="Resolution of webcam feed")
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Load YOLO model (use appropriate model path)
    model = YOLO('best.pt')  # Replace 'best.pt' with your YOLO weights file

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame")
            break

        # Perform inference on the frame using YOLO
        results = model(frame)
        frame = results[0].plot()  # Draw bounding boxes and labels on the frame

        # Display the resulting frame
        cv2.imshow("Live Camera Feed", frame)

        # Exit on pressing 'Esc'
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()