import cv2
from ultralytics import YOLO

# 1. Initialize YOLOv8 Model
model = YOLO('yolov8n.pt')

# 2. Setup Video Capture (0 for webcam, or change to "video.mp4")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Get properties for output saving
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_input = int(cap.get(cv2.CAP_PROP_FPS)) or 30

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('yolo_tracker.mp4', fourcc, fps_input, (frame_width, frame_height))

# 3. Variables for Tracking Analytics
all_tracked_ids = set()  # Keeps track of every unique ID seen over time

print("Pipeline Active. Press 'q' to safely save and exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- AI TRACKING INFERENCE ---
    # persist=True maintains memory between consecutive frames
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", stream=True)

    annotated_frame = frame.copy()
    live_count = 0

    for r in results:
        # Verify that objects with tracking IDs exist in the current frame
        if r.boxes is not None and r.boxes.id is not None:
            # Get the frame with built-in boxes, labels, and IDs drawn by YOLO
            annotated_frame = r.plot()
            
            # Extract tracking IDs as a list of integers
            tracking_ids = r.boxes.id.int().tolist()
            
            # Update analytics variables
            live_count = len(tracking_ids)
            for obj_id in tracking_ids:
                all_tracked_ids.add(obj_id)

    # --- DASHBOARD OVERLAY (Live Count & Unique Count) ---
    # Draw a clean, dark semi-transparent box for the text elements
    cv2.rectangle(annotated_frame, (10, 10), (280, 85), (0, 0, 0), -1)
    
    # Render text strings onto the frame
    cv2.putText(annotated_frame, f"Live On-Screen: {live_count}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    cv2.putText(annotated_frame, f"Total Unique Seen: {len(all_tracked_ids)}", (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

    # 4. Save and Display the Frame
    out.write(annotated_frame)
    cv2.imshow('Real-Time Tracking Analytics', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Clean Shutdown
cap.release()
out.release()
cv2.destroyAllWindows()

print("\n--- Session Summary ---")
print(f"Total unique objects tracked during this run: {len(all_tracked_ids)}")
print("Video saved successfully as 'analytics_output.mp4'")
