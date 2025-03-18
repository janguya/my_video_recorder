import cv2 as cv
import time

# 웹캠 열기 (기본 카메라: 0)
# mac 에서 0 으로 하니까 아이폰으로 연결됨
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

# 웹캠의 실제 FPS 가져오기
BASE_FPS = cap.get(cv.CAP_PROP_FPS)
print(f"BASE_FPS: {BASE_FPS}")
if BASE_FPS == 0 or BASE_FPS > 30.0:
    BASE_FPS = 30.0  # 기본값 설정

fps = BASE_FPS

print(f"📷 웹캠 FPS: {fps}")

recording = False  # 녹화 상태 변수
out = None  # VideoWriter 객체

while True:
    start_time = time.time()  # 프레임 시간 측정

    ret, frame = cap.read()
    if not ret:
        # 카메라가 준비될 때까지 기다리는 로직 추가
        MAX_RETRIES = 30  # 최대 30번 (약 3초 대기)
        retry_count = 0

        while retry_count < MAX_RETRIES:
            ret, frame = cap.read()
            if ret:
                break
            print(f"⏳ 카메라 준비 중... ({retry_count + 1}/{MAX_RETRIES})")
            time.sleep(0.1)  # 0.1초 대기
            retry_count += 1
            print("❌ 프레임을 읽을 수 없습니다.")
            break

    # 🔹 원본 프레임 복사 (녹화용)
    record_frame = frame.copy()
    display_frame = frame.copy()  # 화면 표시용

    # FPS 값을 오른쪽 하단에 추가
    height, width, _ = frame.shape
    fps_text = f"FPS: {int(fps)}"

    # 녹화 중이면 화면에 빨간 원(🔴) 추가
    if recording:
        cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)
    cv.putText(frame, fps_text, (width - 120, height - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv.imshow('Video Recorder', display_frame)

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
    # 녹화 중이면 저장
    if recording and out:
        out.write(record_frame)

    if not recording:
        # ↑ 키 프레임 증가
        if key == '+' or '=':
            if (fps + 5) <= 30:
                fps += 5
                print("🔼 FPS 증가:", fps)
                cap.set(cv.CAP_PROP_POS_FRAMES, fps)
         # ↓ 키 프레임 감소
        elif key == '-' or '_':
            if (fps - 5) >= 5:
                fps -= 5
                print("🔽 FPS 감소:", fps)
                cap.set(cv.CAP_PROP_POS_FRAMES, fps)

    # 프레임 속도 조정 (실제 FPS에 맞추기)
    elapsed_time = time.time() - start_time
    wait_time = max(1 / fps - elapsed_time, 0)
    time.sleep(wait_time)

# 정리
cap.release()
if out:
    out.release()
cv.destroyAllWindows()
