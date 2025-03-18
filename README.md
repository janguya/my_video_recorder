# 🎥 OpenCV Video Recorder  

Python을 사용하여 웹캠 영상을 실시간으로 녹화할 수 있는 프로그램입니다.  

---

## 🖥️ 사용법  

| 키 | 기능 |
|----|------|
| `Space` | 녹화 시작/정지 |
| `ESC` | 프로그램 종료 |
| `↑` | FPS 증가 (+5) |
| `↓` | FPS 감소 (-5) |

---

## 🎞️ 실행 예시  

### ▶ 실행 화면 (GIF)  
![my_video_recorder_example.gif](my_video_recorder_example.gif)  

GIF 파일을 생성하려면, 녹화된 `output.avi`를 `GIF`로 변환하면 됩니다.  

### 🔄 AVI → GIF 변환 방법  
**FFmpeg 사용**  
```bash
ffmpeg -i output.avi -vf "fps=10,scale=640:-1:flags=lanczos" video_recorder.gif
```
- `fps=10` → 10프레임으로 GIF 변환  
- `scale=640:-1` → 가로 640px로 리사이징  

---
