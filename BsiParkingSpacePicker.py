import cv2
import json
import numpy as np

width, height = 210, 440  # Dimenzije parkirnih mjesta

# Dodavanje koordinata parking mjesta.
# Lijevim klikom misa dodajemo parking mjesto.
# Desni klik misa u oznacenom prostoru parking mjesta to parking mjesto se brise
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

# Stream URL
# rtsp_url = "rtsp://admin:Proba123.@192.168.1.64:554/Streaming/channels/101"
# # cap = cv2.VideoCapture(rtsp_url)
cap = cv2.VideoCapture("assets/park-video2.mp4")

# Učitaj prvi frejm. Nema potrebe da ucitavam cijeli video kada je slika uvijek ista,
# parking mjesta se ne pomijeraju, Uzmem prvi frejm i nad njim radi obiljezavanje parking mjesta
# Kada zavrsim sa obiljezavanjem izlazim iz programa pritiskom na slovo "q" na tastaturi.
# Koordiniate ostaju upisane u fajl CarParkPos.json
ret, frame = cap.read()
cap.release()

if not ret:
    raise Exception("Error: Could not read frame from video stream")

# Skaliranje okvira za prikaz
display_width = 1280  # Mozeš prilagoditi ovu vrednost prema svojoj rezoluciji ekrana
frame_scale = display_width / frame.shape[1]
display_height = int(frame.shape[0] * frame_scale)  # Odrzava aspektni odnos
resized_frame = cv2.resize(frame, (display_width, display_height))

while True:
    # Kopiraj originalni frejm za prikaz
    display_frame = resized_frame.copy()

    for pos in posList:
        points = pos["points"]
        scaled_points = [[int(p[0] * frame_scale), int(p[1] * frame_scale)] for p in points]
        cv2.polylines(display_frame, [np.array(scaled_points)], isClosed=True, color=(255, 0, 255), thickness=2)

    cv2.imshow("Image", display_frame)
    cv2.setMouseCallback("Image", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
