import cv2
import os
import numpy as np
import requests
import tkinter as tk

from datetime import date

from carad_display.utils.json import read_data, write_data
from carad_display.utils.gps import is_location_in_poly

import importlib.resources as pkg_resources

FOLDER_PATH = '/tmp/carad_videos/'
WINDOW_NAME = 'Fullscreen Video'
SERVER_URL = 'http://carad.tech/'

def get_availible_videos(cur_date: date):
	try:
		response = requests.get(SERVER_URL + 'videos')
		# Check if the request was successful
		response.raise_for_status()
		# Parse JSON content to a Python dictionary
		data = response.json()
		print (data)
	except Exception:
		print ("No connection to download videos")
	os.makedirs(os.path.join(FOLDER_PATH, str(date.today())), exist_ok=True)

	geopolygons = {
		0: []
	}

	for video in data.get('videos') or []:
		print (video.get('link'))
		
		title = video.get("title").replace(" ", "_")
		response = requests.get(video.get('link'))
		response.raise_for_status()
		file_path = os.path.join(FOLDER_PATH, str(date.today()), title)
		# print (file_path)
		with open(file_path, "wb") as f:
			for chunk in response.iter_content(chunk_size=8192):
				if chunk:  # filter out keep-alive chunks
					f.write(chunk)

		if geopolygon := video.get('geopolygon'):
			geopolygons[geopolygon] = file_path
		else:
			geopolygons[0].append(file_path)

		print(f"File downloaded and saved to: {file_path}")

	print (geopolygons)
	write_data(geopolygons, filepath = os.path.join(FOLDER_PATH, str(date.today()), "geopolygons.json"))


def get_videos(location: list[float, float]) -> list[str]:
	geopolygons = read_data(os.path.join(FOLDER_PATH, str(date.today()), "geopolygons.json"))

	print (type(geopolygons))

	for key in geopolygons.keys():
		print (key, type(key))
		if key != '0':
			if is_location_in_poly(key, location):
				return geopolygons[key], True

	if geopolygons['0']:
		return [geopolygons['0'], False]
	else:
		return [[str(get_path_to_default_video())], False]


def play_video(filepath: str):
	video_path = filepath
	root = tk.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root.destroy()

	# video_path = "your_video.mp4"
	cap = cv2.VideoCapture(video_path)
	from datetime import datetime
	try:
		cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
	except Exception:
		cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
		cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	t = datetime.now()
	h, w = None, None
	i = 0
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break
		if i == 2:
			i = 0
			continue
		else:
			i += 1
		if not h:
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
	# cv2.destroyAllWindows()
	print (datetime.now() - t)
	return 0


def get_path_to_default_video():
	video_path = pkg_resources.files('carad_display.videos').joinpath('default_video.mp4')
	return video_path
