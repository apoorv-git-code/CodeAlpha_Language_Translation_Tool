# ⏳ Real-Time Object Detection and Tracking Dashboard 👀

A real-time Computer Vision pipeline built with Python, OpenCV, and YOLOv8. This application processes a live video feed (webcam or video file), detects objects, and tracks them continuously across frames using the ByteTrack algorithm. It features a live telemetry dashboard overlay displaying real-time tracking analytics.

## ⚙️ Features
* **Real-Time Inference:** High-speed object detection powered by a pre-trained YOLOv8 Nano model.
* **Persistent Object Tracking:** Uses ByteTrack to assign unique, consistent IDs to individual objects across frames.
* **Live Analytics Dashboard:** An on-screen overlay display showing:
  * **Live On-Screen Count:** Number of tracked objects currently in the frame.
  * **Total Unique Seen:** Cumulative count of unique object IDs observed throughout the session (safeguarded against duplicate counting).
* **Automated Recording:** Automatically encodes and saves the processed tracking feed to an output `.mp4` file.

---

## 🚀 Repository Structure 🚀

```text
├── yolo_tracker.py    # Main application script with analytics dashboard
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
└── yolo_tracker.mp4   # Auto-generated recorded output (created after running)
```

## 💻 Setup & Installation

Follow these steps to configure your local environment and run the application.

1. Clone the Repository

    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    
2. 
3. 


