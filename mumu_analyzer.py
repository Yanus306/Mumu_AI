from ultralytics import YOLO
import cv2
import numpy as np
import time  # 1. 시간 측정을 위한 라이브러리 추가

# 1. 모델 로드
model = YOLO("yolov10n.pt")
video_path = "Dog28sVideo.mp4"
cap = cv2.VideoCapture(video_path)

# 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('mumu_anomaly_result.mp4', fourcc, 30.0,
                      (int(cap.get(3)), int(cap.get(4))))

prev_center = None

# --- 분석 시작 시간 기록 ---
start_time = time.time()
print("Mumu가 이상행동 분석을 시작합니다")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # save=False로 설정 (내가 직접 cv2로 글자를 써서 저장할 거니ㄱr..)
    results = model(frame, conf=0.3, verbose=False)

    for r in results:
        # 박스 그리기 및 좌표 추출
        annotated_frame = r.plot()
        boxes = r.boxes
        for box in boxes:
            if int(box.cls) in [15, 16]:  # 개, 고양이
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                current_center = np.array([(x1 + x2) / 2, (y1 + y2) / 2])

                if prev_center is not None:
                    distance = np.linalg.norm(current_center - prev_center)

                    # 이상행동 감지 조건 (움직임이 너무 클 때)
                    if distance > 80:  # 8초 영상에 맞춰 약간 하향 조정
                        cv2.putText(annotated_frame, "WARNING: ABNORMAL MOVEMENT!", (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

                prev_center = current_center

        # 프레임 저장
        out.write(annotated_frame)

cap.release()
out.release()

# --- 분석 종료 및 시간 계산 ---
end_time = time.time()
total_duration = end_time - start_time # 종료 시간 - 시작 시간

print(f"✅ 분석 완료! 총 소요 시간: {total_duration:.2f}초")
print("분석 완료 'mumu_anomaly_result.mp4' 파일을 확인하세요.")

