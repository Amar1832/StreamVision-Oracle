# StreamVision-Oracle

⚡ Real-time video analytics platform built with **FastAPI**, **YOLO-based object detection**, and a lightweight **HTML frontend**.  
It supports live streaming, detection, analytics, and visualization for intelligent video surveillance.

---

## 📂 Project Structure

StreamVision-Oracle/
│── main.py # FastAPI entrypoint
│── streams.py # Handles video stream input
│── detections.py # YOLO object detection logic
│── analytics.py # Post-processing, statistics & insights
│── index.html # Frontend visualization
│── requirements.txt # Python dependencies
│── example.env # Example environment variables
│── README.md # Project documentation
│── 20250808_...mp4 # Sample YOLO output demo video



---

## 🚀 Features

- 🎥 **Stream Handling** → Capture video from webcam, RTSP, or uploaded files  
- 🧠 **YOLO Detection** → Person/object detection in real-time  
- 📊 **Analytics Module** → Counts, anomaly checks, frame-level insights  
- 🌐 **FastAPI Backend** → REST endpoints for detection & analytics  
- 💻 **Frontend (index.html)** → Simple interface to visualize streams & results  
- 📂 **Demo Video Included** → See `20250808_141859_yolo_out...mp4`  

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https:/Amar1832/github.com/<>/StreamVision-Oracle.git
cd StreamVision-Oracle

2️⃣ Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

🔑 Environment Variables

Copy the .env file from example.env and configure:

VIDEO_SOURCE=0          # webcam (0) or path to video file
MODEL_PATH=yolov8n.pt   # YOLO model weights
SAVE_OUTPUT=True        # Save detection output video

▶️ Running the Application
Start FastAPI server:
uvicorn main:app --reload


Server runs at: http://127.0.0.1:8000/

🌐 Frontend

Open index.html in a browser for a simple video/detection dashboard

Connects to FastAPI backend for results

📊 Analytics

analytics.py processes detection logs:

Object counts per frame

Event-based alerts (e.g., multiple persons, restricted zones)

Custom metrics integration

📽️ Example Output

A demo output video has been included:
20250808_141859_yolo_out_20250808_142246.mp4

📌 Roadmap

 Add WebSocket support for real-time updates

 Extend analytics to crowd density estimation

 Deploy to cloud (AWS/GCP) with GPU acceleration

 Build advanced React frontend

🤝 Contributing

Fork this repository

Create your feature branch (git checkout -b feature/my-feature)

Commit your changes (git commit -m 'Add feature')

Push to branch (git push origin feature/my-feature)

Open a Pull Request

📜 License

MIT License © 2025 StreamVision-Oracle Team


---

 
