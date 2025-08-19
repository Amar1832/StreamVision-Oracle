from __future__ import annotations
import cv2
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from ultralytics import YOLO
from ..core.config import YOLO_MODEL
from ..core.db import exec_one
from .streams import STREAMS

router = APIRouter()

model = YOLO(YOLO_MODEL)
NAMES = model.names  # dict idx->label

def _open_capture(src):
    if isinstance(src, str) and src.strip().isdigit():
        src = int(src)
    return cv2.VideoCapture(src)

def _bucket(conf: float) -> str:
    if conf < 0.40: return "RED"
    if conf < 0.60: return "YELLOW"
    return "GREEN"

@router.get("", response_class=JSONResponse)
def get_detections(stream_id: int = Query(..., ge=1),
                   max_frames: int = Query(30, ge=1, le=500),
                   stride: int = Query(5, ge=1, le=50)):
    stream = next((s for s in STREAMS if s.id == stream_id), None)
    if not stream:
        raise HTTPException(404, "Stream not found")
    cap = _open_capture(stream.source)
    if not cap.isOpened():
        raise HTTPException(400, f"Cannot open: {stream.source}")

    out = []
    i = 0
    taken = 0
    people_total = 0
    red = yellow = green = 0

    while taken < max_frames:
        ok, frame = cap.read()
        if not ok: break
        if i % stride:
            i += 1
            continue
        r = model(frame, verbose=False)[0]
        for b in r.boxes:
            cls = int(b.cls[0]) if b.cls is not None else -1
            label = NAMES.get(cls, str(cls))
            if label.lower() != "person":
                continue
            conf = float(b.conf[0] if b.conf is not None else 0.0)
            x1, y1, x2, y2 = b.xyxy[0].int().tolist()
            buck = _bucket(conf)
            if   buck == "RED":    red += 1
            elif buck == "YELLOW": yellow += 1
            else:                  green += 1
            people_total += 1
            out.append({
                "label": label, "conf": round(conf,3), "bucket": buck,
                "x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2),
                "frame": i
            })
        taken += 1
        i += 1
    cap.release()

    return {"stream_id": stream_id,
            "summary": {"total": people_total, "red": red, "yellow": yellow, "green": green,
                        "frames_analyzed": taken, "stride": stride},
            "detections": out}

@router.get("/video_feed")
def video_feed(stream_id: int = Query(..., ge=1),
               recording_id: int | None = Query(None, ge=1)):
    stream = next((s for s in STREAMS if s.id == stream_id), None)
    if not stream:
        raise HTTPException(404, "Stream not found")
    cap = _open_capture(stream.source)
    if not cap.isOpened():
        raise HTTPException(400, f"Cannot open: {stream.source}")

    def gen():
        try:
            while True:
                ok, frame = cap.read()
                if not ok: break
                r = model(frame, verbose=False)[0]

                people = 0
                red = yellow = green = 0

                for b in r.boxes:
                    cls = int(b.cls[0]) if b.cls is not None else -1
                    label = NAMES.get(cls, str(cls))
                    if label.lower() != "person":
                        continue
                    people += 1
                    conf = float(b.conf[0] if b.conf is not None else 0.0)
                    x1, y1, x2, y2 = b.xyxy[0].int().tolist()
                    buck = _bucket(conf)
                    if   buck == "RED":    color = (0,0,255);   red += 1
                    elif buck == "YELLOW": color = (0,255,255); yellow += 1
                    else:                  color = (0,200,0);  green += 1

                    cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                    cv2.putText(frame, f"person {int(conf*100)}% {buck}",
                                (x1, max(18,y1-6)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

                cv2.putText(frame, f"Persons: {people}  R:{red} Y:{yellow} G:{green}",
                            (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

                if recording_id:
                    exec_one(
                        """INSERT INTO DETECTION_SNAPSHOTS
                               (RECORDING_ID, STREAM_ID, PERSONS_TOTAL, RED_COUNT, YELLOW_COUNT, GREEN_COUNT)
                               VALUES (:rid, :sid, :tot, :r, :y, :g)""" ,
                        {"rid": recording_id, "sid": stream_id, "tot": people,
                         "r": red, "y": yellow, "g": green}
                    )

                ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if not ok: continue
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")
        finally:
            cap.release()

    return StreamingResponse(gen(), media_type="multipart/x-mixed-replace; boundary=frame")
