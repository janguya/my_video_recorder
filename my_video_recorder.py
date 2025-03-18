import cv2 as cv
import time

# 웹캠 열기 (기본 카메라: 0)
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

# 웹캠의 실제 FPS 가져오기
fps = cap.get(cv.CAP_PROP_FPS)
if fps == 0 or fps > 30.0:
    fps = 30.0  # 기본값 설정

print(f"📷 웹캠 FPS: {fps}")

recording = False  # 녹화 상태 변수
out = None  # VideoWriter 객체

while True:
    start_time = time.time()  # 프레임 시간 측정

    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다.")
        break

    # 녹화 중이면 화면에 빨간 원(🔴) 추가
    if recording:
        cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)

    cv.imshow('Video Recorder', frame)

    key = cv.waitKey(1) & 0xFF

    if key == 27:  # ESC 키 → 종료
        break
    elif key == 32:  # Space 키 → 녹화 토글
        recording = not recording
        print("🔴 녹화 시작" if recording else "⏹ 녹화 중지")

        if recording:
            # 녹화 시작 시 VideoWriter 객체 생성
            fourcc = cv.VideoWriter_fourcc(*'XVID')  # 코덱 설정
            height, width, _ = frame.shape  # 현재 프레임 크기 가져오기
            out = cv.VideoWriter('output.avi', fourcc, fps, (width, height))
        else:
            # 녹화 중지 시 VideoWriter 해제
            if out:
                out.release()
                out = None

    # ↑ 키 프레임 증가
    elif key == 82:
        if (fps + 5) <= 30:
            fps += 5
        cap.set(cv.CAP_PROP_POS_FRAMES, fps)
    # ↓ 키 프레임 감소
    elif key == 84:
        if (fps - 5) >= 5:
            fps -= 5
        cap.set(cv.CAP_PROP_POS_FRAMES, fps)

    # 녹화 중이면 저장
    if recording and out:
        out.write(frame)

    # 프레임 속도 조정 (실제 FPS에 맞추기)
    elapsed_time = time.time() - start_time
    wait_time = max(1 / fps - elapsed_time, 0)
    time.sleep(wait_time)

# 정리
cap.release()
if out:
    out.release()
cv.destroyAllWindows()
