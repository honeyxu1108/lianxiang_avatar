import cv2
import numpy as np
import subprocess

def extract_frames(video_clip):
    return [frame for frame in video_clip.iter_frames()]

def crop_video(image, video, x, y, side_length):
    x0 = x
    y0 = y
    x1 = x0 + side_length
    y1 = y0 + side_length
    
    h, w = image.shape[:2]

    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)


    width = x1 - x0
    height = y1 - y0


    side_length = min(width, height)


    center_x = (x0 + x1) // 2
    center_y = (y0 + y1) // 2

    new_x0 = max(0, center_x - side_length // 2)
    new_y0 = max(0, center_y - side_length // 2)
    new_x1 = min(w, new_x0 + side_length)
    new_y1 = min(h, new_y0 + side_length)


    if (new_x1 - new_x0) != (new_y1 - new_y0):
        side_length = min(new_x1 - new_x0, new_y1 - new_y0)
        new_x1 = new_x0 + side_length
        new_y1 = new_y0 + side_length

    cropped_clip = video.crop(x1=new_x0, y1=new_y0, x2=new_x1, y2=new_y1)


    return cropped_clip


def capture_first_frame(video_path, output_path):  
 
    # build ffmpeg command  
    command = [  
        'ffmpeg',  
        '-i', video_path,
        '-ss', '00:00:00',
        '-frames:v', '1',
        output_path
    ]  
      
    # execute 
    try:  
        subprocess.run(command, check=True)  
        print(f"成功截取第一帧并保存到 {output_path}")  
    except subprocess.CalledProcessError as e:  
        print(f"发生错误：{e}")  