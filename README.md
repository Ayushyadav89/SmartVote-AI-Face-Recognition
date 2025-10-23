# 🗳️ Smart Voting System (Face Recognition Based)

## 📌 Overview
- The Smart Voting System is a Python-based application that ensures secure and efficient electronic voting using Face Recognition.
It allows voters to register their details with a photo and later cast their vote using facial recognition. The system uses the KNeighborsClassifier algorithm from scikit-learn for face recognition and stores voter data in a CSV file for record-keeping.

- This project provides a more transparent, secure, and user-friendly approach to voting while reducing fraudulent practices.

## ⚙️ Features

- ✅ Voter Registration – Users can register with their personal details and captured face image.

- ✅ Face Recognition Voting – Authenticate voters using OpenCV and KNN classifier.

- ✅ Multiple Parties Support – Voters can choose among:
  1. BJP 🟠
  2. Congress 🟢
  3. AAP 🟡
  4. NOTA ❌

- ✅ CSV Data Storage – Saves voter information and voting logs.

- ✅ Time-stamped Votes – Keeps record of vote time and date.

- ✅ Prevents Multiple Votes – Each voter can vote only once.

## 🛠️ Tech Stack

- Python 3.x
- 
- OpenCV (cv2) – For face detection & recognition

- scikit-learn (KNeighborsClassifier) – ML model for classification

- NumPy & Pandas – Data handling

- CSV module – For storing voter data and votes

- pickle – For model persistence


## 🚀 How It Works

1. Registration

- User provides details (Name, ID, etc.).

- Face image captured using webcam (OpenCV).

- Details saved in  voter_data.csv.

2. Training

- Captured images are trained using KNeighborsClassifier.

- Trained model stored using pickle.

3. Voting

- Voter shows face on webcam.

- System verifies using trained KNN model.

- If verified and not voted earlier → voter can cast vote for BJP, Congress, AAP, or NOTA.

- Vote saved in votes.csv with timestamp.

## 🖥️ Installation & Usage
1. Clone Repository
- git clone https://github.com/Ayushyadav89/SmartVote-AI-Face-Recognition.git
- cd SmartVote-AI-Face-Recognition

2. Install Dependencies
- pip install opencv-python scikit-learn numpy pandas pywin32

3. Run Modules
- Register a Voter
- python add_faces.py

4. Train the Model
- Data Folder: faces_data.pkl and names.pkl

5. Start Voting
- python give_vote.py

## 📊 Sample CSV Files
- Votes.csv

- VoterID, Party, FaceDataPath, RegisteredTime
- 1234,BJP,06-09-2025,11-10-47


## 🔐 Security Features

- Prevents duplicate voting using voter ID check.

- Facial recognition ensures only registered voters can vote.

- Voting logs are stored securely in CSV files.

## 📌 Future Enhancements

- Add GUI Dashboard using Tkinter/Streamlit.

- Integrate Blockchain for tamper-proof voting.

- Support for real-time results visualization.

## 📜 License

- This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/Ayushyadav89/SmartVote-AI-Face-Recognition.git) file for details.

## 👨‍💻 Author

- Ayush Yadav
- B.Tech CSE | MERN & Python Developer | AI/ML Enthusiast
- LinkedIn : [Link](https://www.linkedin.com/in/ayush-yadav-143536253/)
- Gmail ID : 2k22.cse.2213307@gmail.com
