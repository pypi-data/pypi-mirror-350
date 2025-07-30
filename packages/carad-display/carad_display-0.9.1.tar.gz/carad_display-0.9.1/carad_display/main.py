import asyncio
import cv2
from datetime import date
import os
import tkinter as tk
import numpy as np

from carad_display.utils.metrics import send_metrica
from carad_display.utils.videos import get_availible_videos, get_path_to_default_video, get_videos, play_video, WINDOW_NAME
from carad_display.utils.gps import get_gps


def default_pic():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    window_name = "Fullscreen Video"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap = cv2.VideoCapture(get_path_to_default_video())
    # sudo apt-get install unclutter
    try:
        os.system('unclutter -idle 0.5 &')
    except Exception:
        pass
    ret = None
    while not ret:
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                ...

            # Get original frame size
            h, w = frame.shape[:2]

            # Calculate scale to fit screen while maintaining aspect ratio
            scale_w = screen_width / w
            scale_h = screen_height / h
            scale = min(scale_w, scale_h)


            # Calculate new dimensions
            new_w = int(w * scale)
            new_h = int(h * scale)
            black_bg = 0 * np.ones((screen_height, screen_width, 3), dtype=np.uint8)
            x_offset = (screen_width - new_w) // 2
            y_offset = (screen_height - new_h) // 2

            resized_frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
            black_bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_frame

            cv2.imshow(WINDOW_NAME, black_bg)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            cap.release()


def main():
    default_pic()
    # getting today day
    current_day = date.today()
    # getting links for videos on today
    get_availible_videos(current_day)

    location = get_gps()
    videos_old, is_poly_old = get_videos(location)
    print (type(videos_old), videos_old)
    while 1:
        for video in videos_old:
            videos, is_poly = get_videos(location)
            play_video(video)
            send_metrica(video.split('/')[-1])
            if not is_poly_old and is_poly:
                videos_old = videos
            elif len(videos_old) == 1:
                videos_old.extend(videos)


if __name__ == "__main__":
    asyncio.run(main())
