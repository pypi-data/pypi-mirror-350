# pip install opencv-python numpy windows-curses


#####################################################################################
# This module play mp4 video in terminal, with ascii characters
#####################################################################################
# Distribution steps
#------------------------------------------------------------------------------------
# 1. install required tools
#    > pip install setuptools wheel twine build
# 2. prepare pyproject.toml
#    > python -m build
# 
# 1. You can also install the whl or gz file directly (in other machine / virtual env)
# > pip install dist/<WHL_FILENAME>.whl
# OR
# > pip install dist/<COMPRESSED_FILENAME>.tar.gz
#------------------------------------------------------------------------------------
# upload them to pypi (register from https://pypi.org, get API token)
# > twine upload dist/*
#   ...
#   https://pypi.org/project/ascii-mp4-video-player-exp/0.29
#
# (in other machine / virtual env)
# > pip install ascii_mp4_video_player_exp

import cv2
import numpy as np
import curses
import time
import os

ASCII_CHARS = [
    ' ', '·', '.', ':', '-', '+', '=', '*', 'O', 'o', 'I',
    'i', '?', '!', '[', ']', '{', '}', '(', ')', '<', '>',
    'v', 'x', 'X', '&', '#', '%', '$', '@', 'M', 'W'
]

def video_frame_to_ascii(frame, term_w, term_h, term_scale=0.5):
    # Pre-downsample to reduce OpenCV load
    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)

    height, width, _ = frame.shape
    aspect_ratio = height / width

    new_width = int(term_w * term_scale)
    new_height = int(aspect_ratio * new_width * 0.55)

    if new_width < 10 or new_height < 5:
        return "Window too small."

    resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    gray = gray.astype(np.float32)
    brightness_indices = (gray * (len(ASCII_CHARS) - 1) / 255).astype(np.uint8)

    chars = np.take(ASCII_CHARS, brightness_indices)
    return "\n".join("".join(row) for row in chars)

def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def draw_frame(stdscr, ascii_frame, progress_footer, term_h, term_w):
    try:
        for y, line in enumerate(ascii_frame.split('\n')):
            if y >= term_h - 1:
                break
            stdscr.addstr(y, 0, line[:term_w - 1])

        if progress_footer:
            stdscr.addstr(term_h - 1, 0, progress_footer[:term_w - 1])

        stdscr.refresh()
    except curses.error:
        pass

def skip_frames(cap, target_frame, current_frame):
    while current_frame < target_frame:
        ret, _ = cap.read()
        if not ret:
            break
        current_frame += 1
    return current_frame

def init_and_play(stdscr, cap, delay, term_scale, loop=False, video_path=None):
    if video_path is None:
        raise ValueError("video_path must be provided for looping or seeking")

    curses.curs_set(0)
    stdscr.nodelay(True)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 24
    total_duration = total_frames / video_fps if video_fps > 0 else 0
    cached_total_time = format_time(total_duration)

    current_frame = 0
    last_progress_update = -1
    progress_footer = ""
    last_term_size = stdscr.getmaxyx()
    paused = False
    seek_needed = False
    last_frame = None  # To store the last rendered frame

    while True:
        # Seek only if needed
        if seek_needed:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            seek_needed = False

        term_h, term_w = stdscr.getmaxyx()
        if (term_h, term_w) != last_term_size:
            stdscr.clear()
            last_term_size = (term_h, term_w)

        # Only read new frame if not paused
        if not paused:
            ret, frame = cap.read()
            if ret:
                last_frame = frame.copy()
            else:
                if loop:
                    cap.release()
                    cap = cv2.VideoCapture(video_path)
                    if not cap.isOpened():
                        break
                    current_frame = 0
                    continue
                else:
                    break
        else:
            # Use last known frame
            frame = last_frame
            ret = frame is not None

        if not ret:
            break

        ascii_frame = video_frame_to_ascii(frame, term_w, term_h - 1, term_scale=term_scale)

        current_time = current_frame / video_fps if video_fps > 0 else 0
        status = "Playing" if not paused else "Paused"
        progress_footer = f"{status} - {format_time(current_time)}/{cached_total_time}"
        if int(current_time) != last_progress_update:
            last_progress_update = int(current_time)

        draw_frame(stdscr, ascii_frame, progress_footer, term_h, term_w)

        time.sleep(delay)

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):  # Toggle pause/resume
            paused = not paused
            current_time = current_frame / video_fps if video_fps > 0 else 0
            status = "Playing" if not paused else "Paused"
            progress_footer = f"{status} - {format_time(current_time)}/{cached_total_time}"
            last_progress_update = int(current_time)
        elif key == curses.KEY_LEFT:
            step = max(int(0.01 * total_frames), int(video_fps * 5))  # ~1% or 5s
            new_frame = max(0, current_frame - step)
            if new_frame < current_frame:
                cap.release()
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    break
                current_frame = skip_frames(cap, new_frame, 0)
                ret, frame = cap.read()
                if ret:
                    last_frame = frame.copy()
            current_time = current_frame / video_fps if video_fps > 0 else 0
            status = "Playing" if not paused else "Paused"
            progress_footer = f"{status} - {format_time(current_time)}/{cached_total_time}"
            last_progress_update = int(current_time)
        elif key == curses.KEY_RIGHT:
            step = max(int(0.01 * total_frames), int(video_fps * 5))  # ~1% or 5s
            new_frame = min(total_frames - 1, current_frame + step)
            if new_frame > current_frame:
                current_frame = skip_frames(cap, new_frame, current_frame)
                ret, frame = cap.read()
                if ret:
                    last_frame = frame.copy()
            current_time = current_frame / video_fps if video_fps > 0 else 0
            status = "Playing" if not paused else "Paused"
            progress_footer = f"{status} - {format_time(current_time)}/{cached_total_time}"
            last_progress_update = int(current_time)

        if not paused:
            current_frame += 1

def play_ascii_video(video_path, fps=24, term_scale=0.5, loop=True):
    if not os.path.exists(video_path):
        print(f"Error: File not found - {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    delay = 1.0 / fps

    try:
        args = (cap, delay, term_scale, loop, video_path)
        curses.wrapper(init_and_play, *args)
    except Exception as e:
        print(f"Playback error: {e}")
    finally:
        cap.release()
        print("Video playback ended.")


if __name__ == "__main__":
    # video downloaded from: https://www.pexels.com/zh-cn/video/855401/   
    mp4_file = r"D:\Users\paul\Pictures\pexels_855401-uhd_3840_2160_25fps.mp4"

    # Controls:
    # - Space: Pause/Resume
    # - ← Left Arrow: Seek Backward
    # - → Right Arrow: Seek Forward
    # - Q: Quit

    play_ascii_video(mp4_file, fps=24, term_scale=0.5)