from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# -------------------- Helpers --------------------
def speak(text):
    try:
        Dispatch("SAPI.SpVoice").Speak(text)
    except Exception:
        pass  # don't crash if SAPI isn't available

def check_if_exists(value, path="Votes.csv"):
    try:
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == value:
                    return True
    except FileNotFoundError:
        return False
    return False

def fit_into_box(img, box_w, box_h, margin=10):
    """
    Resize 'img' to fit into a box (box_w x box_h) keeping aspect ratio,
    and leave a small margin on all sides.
    Returns the resized image.
    """
    box_w = max(1, box_w - 2*margin)
    box_h = max(1, box_h - 2*margin)

    h, w = img.shape[:2]
    scale = min(box_w / w, box_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

# -------------------- Setup --------------------
# Webcam
video = cv2.VideoCapture(0)
facesdetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Data folder
os.makedirs("data", exist_ok=True)

# Load saved labels and face data
with open("data/names.pkl", "rb") as f:
    LABELS = pickle.load(f)
with open("data/faces_data.pkl", "rb") as f:
    FACES = pickle.load(f)

# Train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load background UI
imgBackground = cv2.imread("background.png")
if imgBackground is None:
    raise FileNotFoundError("background.png not found in current folder.")

COL_NAME = ["NAME", "VOTE", "DATE", "TIME"]

# Window
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 1200, 800)

# -------------------- UI Layout (relative) --------------------
# Use relative percentages so it adapts to your background image
Bh, Bw = imgBackground.shape[:2]

# These ratios are tuned for your design (left white panel).
# Tweak slightly if your PNG is different:
# Adjusted ratios so video stays fully in white area
LEFT_X_RATIO   = 0.085   # move a bit right
RIGHT_X_RATIO  = 0.545   # stop earlier (before blue area)
TOP_Y_RATIO    = 0.255   # move a bit down
BOTTOM_Y_RATIO = 0.815   # move up a little

left_x   = int(Bw * LEFT_X_RATIO)
right_x  = int(Bw * RIGHT_X_RATIO)
top_y    = int(Bh * TOP_Y_RATIO)
bottom_y = int(Bh * BOTTOM_Y_RATIO)

box_w = right_x - left_x
box_h = bottom_y - top_y

# -------------------- Main Loop --------------------
while True:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facesdetect.detectMultiScale(gray, 1.3, 5)

    # Default if no face detected yet
    output = [""]

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        # Draw face box & label on the live frame before compositing
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (0, 0, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-12),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

    # Prepare composite
    canvas = imgBackground.copy()

    # Resize the webcam feed to fit nicely inside the left white area (centered)
    frame_resized = fit_into_box(frame, box_w, box_h, margin=18)
    fh, fw = frame_resized.shape[:2]
    start_x = left_x + (box_w - fw) // 2
    start_y = top_y  + (box_h - fh) // 2
    canvas[start_y:start_y+fh, start_x:start_x+fw] = frame_resized

    cv2.imshow("frame", canvas)
    k = cv2.waitKey(1) & 0xFF

    # Prepare timestamp & CSV presence each loop (so it's always defined)
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")
    csv_exists = os.path.isfile("Votes.csv")

    # Block double-voting as soon as we know who it is
    if output[0] != "":
        if check_if_exists(output[0]):
            print("YOU HAVE ALREADY VOTED")
            speak("YOU HAVE ALREADY VOTED")
            break

    # Vote handlers
    def write_vote(party):
        speak("YOUR VOTE HAS BEEN RECORDED")
        time.sleep(1.5)
        with open("Votes.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not csv_exists:
                writer.writerow(COL_NAME)
            writer.writerow([output[0], party, date, timestamp])
        speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")

    if k == ord('1'):
        write_vote("BJP")
        break
    if k == ord('2'):
        write_vote("CONGRESS")
        break
    if k == ord('3'):
        write_vote("AAP")
        break
    if k == ord('4'):
        write_vote("NOTA")
        break
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
