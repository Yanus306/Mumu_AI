from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np
import time
import os
import shutil
import datetime

app = FastAPI()

# 1. 모델 로드 (서버 시작 시 한 번만 로드 => 효율성 증대)
model = YOLO("yolov10n.pt")

# 결과 저장 폴더 설정
RESULT_DIR = "results"
os.makedirs(RESULT_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    # 2. 앱에서 보낸 영상 임시 저장
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2-1 날짜별 결과 폴더 생성 로직
    # results/2026-02-24/ 폴더 안에 저장하기
    today = datetime.date.today().isoformat()
    daily_dir = os.path.join(RESULT_DIR, today)
    os.makedirs(daily_dir, exist_ok=True) # 폴더가 없으면 자동 생성

    cap = cv2.VideoCapture(temp_path)
    video_name = file.filename.split('.')[0]

    # 저장 경로를 날짜별 폴더(daily_dir) 안으로 설정
    output_path = os.path.join(RESULT_DIR, f"{video_name}_result.mp4")
    # ----------------------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0,
                          (int(cap.get(3)), int(cap.get(4))))

    prev_center = None
    anomaly_detected = False  # 이상행동 발생 여부 체크용
    start_time = time.time()

    # 3. 분석 루프 (개/고양이 전용 인식 적용)
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # classes=[15, 16]으로 개, 고양이만 집중 분석
        results = model(frame, conf=0.3, verbose=False, classes=[15, 16])

        for r in results:
            annotated_frame = r.plot()
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                current_center = np.array([(x1 + x2) / 2, (y1 + y2) / 2])

                if prev_center is not None:
                    distance = np.linalg.norm(current_center - prev_center)
                    if distance > 80:  # 설정한 활동거리 임계값
                        anomaly_detected = True
                        cv2.putText(annotated_frame, "WARNING: ABNORMAL MOVEMENT!", (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                prev_center = current_center
            out.write(annotated_frame)

    cap.release()
    out.release()
    os.remove(temp_path)  # 임시 파일 삭제

    total_duration = time.time() - start_time

    # 4. 백엔드 및 안드로이드로 보낼 최종 결과값
    return {
        "status": "success",
        "video_name": video_name,
        "anomaly_detected": anomaly_detected,
        "total_duration": f"{total_duration:.2f}s",
        "result_url": f"http://220.69.241.185:8000/download/{os.path.basename(output_path)}"
    }