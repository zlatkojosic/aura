import cv2
import json
import numpy as np

width, height = 220, 440  # Dimenzije parkirnih mesta

def mouseClick(events, x, y, flags, params):
    global frame_scale
    if events == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = int(x / frame_scale), int(y / frame_scale)
        posList.append({
            "points": [
                [x1, y1],
                [x1, y1 + height],
                [x1 + width, y1 + height],
                [x1 + width, y1]
            ]
        })
    if events == cv2.EVENT_RBUTTONDOWN:
        x = int(x / frame_scale)
        y = int(y / frame_scale)
        for i, pos in enumerate(posList):
            points = pos["points"]
            if points[0][0] < x < points[2][0] and points[0][1] < y < points[2][1]:
                posList.pop(i)
                break

    with open('CarParkPos.json', 'w') as f:
        json.dump(posList, f, indent=4)

# Učitaj koordinate parkirnih mesta iz JSON fajla
try:
    with open('CarParkPos.json', 'r') as f:
        posList = json.load(f)
except FileNotFoundError:
    posList = []

# Proveri da li su koordinate u ispravnom formatu
if posList and isinstance(posList[0], list):
    # Konvertuj staru strukturu u novu
    posList = [{"points": [[x, y], [x, y + height], [x + width, y + height], [x + width, y]]} for x, y in posList]

# Stream URL
# rtsp_url = "rtsp://admin:Proba123.@192.168.1.64:554/Streaming/channels/101"
# cap = cv2.VideoCapture(rtsp_url)
cap = cv2.VideoCapture("assets/park-video2.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Skaliranje okvira za prikaz
    display_width = 800  # Možeš prilagoditi ovu vrednost prema svojoj potrebi
    frame_scale = display_width / frame.shape[1]
    display_height = int(frame.shape[0] * frame_scale)  # Održava aspektni odnos
    resized_frame = cv2.resize(frame, (display_width, display_height))

    for pos in posList:
        points = pos["points"]
        scaled_points = [[int(p[0] * frame_scale), int(p[1] * frame_scale)] for p in points]
        cv2.polylines(resized_frame, [np.array(scaled_points)], isClosed=True, color=(255, 0, 255), thickness=2)

    cv2.imshow("Image", resized_frame)
    cv2.setMouseCallback("Image", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
