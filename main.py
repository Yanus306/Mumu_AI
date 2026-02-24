from ultralytics import YOLO

# 1. 서버에 있는 모델 파일 로드
# 폴더에 있는 yolov10n.pt 바로 사용
model = YOLO("yolov10n.pt")

# 2. 분석할 영상 파일명 (파일 확장자까지 정확히 적어주세요!)
# 예: "my_dog.mp4" 또는 "cat_test.mov"
video_path = "Cat8sVideo.mp4"

# 3. 객체 탐지 수행
# conf=0.3: 30% 이상의 확신이 있을 때만 표시 (MVP용으로 적당함)
# save=True: 결과 영상을 runs/detect/predict 폴더에 저장
results = model.predict(source=video_path, conf=0.3, save=True)

print("무무(Mumu) 분석 완료!")
print("결과는 'runs/detect/' 폴더 안에서 확인할 수 있습니다.")