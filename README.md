# 🎥 OpenCV Video Recorder  

Python을 사용하여 웹캠 영상을 실시간으로 녹화할 수 있는 프로그램입니다.  

---

## 🖥️ 사용법  

| 키        | 기능 |
|----------|------|
| `Space`  | 녹화 시작/정지 |
| `ESC`    | 프로그램 종료 |
| `+ or =` | FPS 증가 (+5) |
| `- or _` | FPS 감소 (-5) |

---

## 🎞️ 실행 예시  

### ▶ 실행 화면 (GIF)  
![my_video_recorder_example.gif](my_video_recorder_example.gif)  

mac 에 연결되어있는 아이폰이 있으면 기본 카메라 0 이 아이폰으로 설정되어 아이폰으로 촬영한 예시.  
mac 화면에는 빨간점이 표시되지만 제일 상단의 화면을 잘 보면 실제로는 녹화되지 않음.  
아이폰이 연결되어 있는 상태에서 mac 내장캠을 사용하고 싶다면
```python
cap = cv2.VideoCapture(1)
```
