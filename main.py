import cv2

from ultralytics import solutions

# Video capture
cap = cv2.VideoCapture("assets/park-video2.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("parking management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize parking management object
parking_manager = solutions.ParkingManagement(
    model="yolo11n.pt",  # path to model file
    # model="yolov8n.pt",  # path to model file
    json_file="CarParkPos.json",  # path to parking annotations file
)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break
    im0 = parking_manager.process_data(im0)
    # im0 = parking_manager.process_data("Assets/test2.png")
    # im0 = parking_manager.process_image("Assets/test2.png")xx
    video_writer.write(im0)
    # Display the frame
    cv2.imshow("Parking Management Video", im0)

    # Wait for the user to press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()