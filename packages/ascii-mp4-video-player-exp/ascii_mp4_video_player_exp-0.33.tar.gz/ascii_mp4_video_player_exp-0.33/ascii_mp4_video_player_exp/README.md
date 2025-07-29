# ASCII MP4 Video Player (Experimental)

A simple Python module that plays MP4 videos in your terminal using ASCII characters.  
Great for fun visualizations or retro-style video playback!

---

## Installation

Install from PyPI using pip:

```bash
pip install ascii-mp4-video-player-exp
```

To use it:

```python
from ascii_mp4_video_player_exp.ascii_player import play_ascii_video

if __name__ == "__main__":
    mp4_file = r"video.mp4"

    # Play mp4 video in termimal
    play_ascii_video(mp4_file, fps=30, term_scale=0.5)
```