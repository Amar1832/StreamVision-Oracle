# 🚀 StreamVision-Oracle

Real-time video analytics system powered by **YOLO object detection** and **FastAPI** backend, 
with a lightweight frontend for visualization.

---

## ✨ Features
- 📹 Live video stream processing (webcam / video files)
- 🎯 Object detection using YOLO
- 📊 Analytics & insights on detections
- 💾 Save processed output videos
- 🌐 FastAPI backend + simple HTML frontend
- 🔌 Easily configurable via `.env`

---

## 📂 Project Structure

```
StreamVision-Oracle/
├── main.py          # FastAPI entrypoint
├── streams.py       # Handles video stream input
├── detections.py    # YOLO object detection logic
├── analytics.py     # Post-processing, statistics & insights
├── index.html       # Frontend visualization
├── requirements.txt # Python dependencies
├── example.env      # Example environment variables
├── README.md        # Project documentation
└── 20250808_...mp4  # Sample YOLO output demo video
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Amar1832/StreamVision-Oracle.git
cd StreamVision-Oracle
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate    # On Linux/Mac
.venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 Environment Variables
Copy the `.env` file from `example.env` and configure:

```ini
VIDEO_SOURCE=0          # webcam (0) or path to video file
MODEL_PATH=yolov8n.pt   # YOLO model weights
SAVE_OUTPUT=True        # Save detection output video
```

### ▶️ Running the Application
Start FastAPI server:
```bash
uvicorn main:app --reload
```

Open browser at:
```
http://127.0.0.1:8000
```

---

## 📊 Output Example

Sample YOLO detection video is included:  
`20250808_...mp4`

![Sample Output](./f6c401e2-ff89-4263-8888-35df4bb733bf.png)

---

## 🚀 Roadmap
- Add person re-identification
- Extend analytics to crowd density estimation
- Deploy to cloud (AWS/GCP) with GPU acceleration
- Build advanced React frontend

---

## 🤝 Contributing

1. Fork this repository  
2. Create your feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m 'Add feature'`)  
4. Push to branch (`git push origin feature/my-feature`)  
5. Open a Pull Request  

---

## 📜 License

MIT License © 2025 StreamVision-Oracle Team

---

