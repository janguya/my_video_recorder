import cv2 as cv
import time

# 웹캠 열기 (기본 카메라: 0)
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

# 웹캠의 FPS 가져오기
BASE_FPS = cap.get(cv.CAP_PROP_FPS)
if BASE_FPS == 0 or BASE_FPS > 30.0:
    BASE_FPS = 30.0  # 기본값 설정

fps = BASE_FPS
print(f"📷 웹캠 FPS: {fps}")

recording = False  # 녹화 상태 변수
out = None  # VideoWriter 객체

while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다.")
        break

    # 원본 프레임 복사 (녹화용)
    record_frame = frame.copy()
    display_frame = frame.copy()  # 화면 표시용

    height, width, _ = frame.shape
    fps_text = f"FPS: {int(fps)}"

    cv.putText(display_frame, fps_text, (width - 120, height - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # 🔴 녹화 중이면 화면에 빨간 원 추가 (녹화 영상에는 포함되지 않음)
    if recording:
        cv.circle(display_frame, (50, 50), 10, (0, 0, 255), -1)

    cv.imshow('Video Recorder', display_frame)

    key = cv.waitKey(1) & 0xFF

    if key == 27:  # ESC 키 → 종료
        break
    elif key == 32:  # Space 키 → 녹화 토글
        recording = not recording
        print("🔴 녹화 시작" if recording else "⏹ 녹화 중지")

        if recording:
            fourcc = cv.VideoWriter_fourcc(*'XVID')  # 코덱 설정
            out = cv.VideoWriter('output.avi', fourcc, fps, (width, height))
        else:
            if out:
                out.release()
                out = None

    # 녹화 중이면 원본 프레임(record_frame)만 저장
    if recording and out:
        out.write(record_frame)

    elapsed_time = time.time() - start_time
    wait_time = max(1 / fps - elapsed_time, 0)
    time.sleep(wait_time)

# 정리
cap.release()
if out:
    out.release()
cv.destroyAllWindows()
