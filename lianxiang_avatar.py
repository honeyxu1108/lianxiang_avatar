from MODNet.demo.video_matting.custom.run_matting import Modnet
from moviepy.editor import ImageSequenceClip, ImageClip, CompositeVideoClip, AudioFileClip
import os
from PIL import Image
import numpy as np
import subprocess

class Final_process:
    def __init__(self):
        pass

    def run_ffmpeg_command(self, cmd):
        try:  
            subprocess.run(cmd, shell=True, check=True)  
        except subprocess.CalledProcessError as e:  
            print(f"Error executing command: {e}")

    def delete_all_files_in_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def composite_images(self, output_vid_path, foreground_dir, audio_path, background_path, scale_ratio, position, output_video_path, fps=24):
        # generate images without green
        mod = Modnet(foreground_dir)
        mod.gen_video_without_green(output_vid_path)

        # Get the list of foreground image files
        foreground_files = sorted([os.path.join(foreground_dir, f) for f in os.listdir(foreground_dir) if f.endswith('.png')])
        
        # Read images with alpha channel using PIL
        frames = []
        for file in foreground_files:
            img = Image.open(file).convert("RGBA")  # Ensure RGBA format
            frames.append(np.array(img))  # Convert to numpy array
        # Read the foreground image sequence using ImageSequenceClip
        foreground_clip = ImageSequenceClip(frames, fps=fps)
        print(foreground_clip.get_frame(0).shape)

        if background_path is None:
            # If background_path is None, directly use the foreground clip as the composite clip
            composite_clip = foreground_clip
        else:
            # Open the background image
            background_clip = ImageClip(background_path).set_duration(foreground_clip.duration)

            # Calculate the width and height of the background image
            background_width, background_height = background_clip.size

            # Resize the foreground image according to the scale ratio
            scaled_foreground_clip = foreground_clip.resize(scale_ratio)

            # Calculate the width and height of the scaled foreground image
            foreground_width, foreground_height = scaled_foreground_clip.size

            # Calculate the position of the foreground image on the background image
            x_pos, y_pos = position

            # Handle the case where the foreground image exceeds the left or right boundary of the background image
            if x_pos < 0:
                scaled_foreground_clip = scaled_foreground_clip.crop(x1=-x_pos, y1=0, x2=foreground_width, y2=foreground_height)
                x_pos = 0
                foreground_width = scaled_foreground_clip.w

            if x_pos + foreground_width > background_width:
                scaled_foreground_clip = scaled_foreground_clip.crop(x1=0, y1=0, x2=background_width - x_pos, y2=foreground_height)
                foreground_width = scaled_foreground_clip.w

            # Handle the case where the foreground image exceeds the top or bottom boundary of the background image
            if y_pos < 0:
                scaled_foreground_clip = scaled_foreground_clip.crop(x1=0, y1=-y_pos, x2=foreground_width, y2=foreground_height)
                y_pos = 0
                foreground_height = scaled_foreground_clip.h

            if y_pos + foreground_height > background_height:
                scaled_foreground_clip = scaled_foreground_clip.crop(x1=0, y1=0, x2=foreground_width, y2=background_height - y_pos)
                foreground_height = scaled_foreground_clip.h

            # Composite the foreground image with the background image
            composite_clip = CompositeVideoClip([background_clip, scaled_foreground_clip.set_position((x_pos, y_pos))])

        # load audio
        audio_clip = AudioFileClip(audio_path)

        # Save the composite video file
        if background_path is None:
            frames_rgb = []
            for frame in frames:  # frame: (H, W, 4)
                rgb = frame[..., :3]
                alpha = frame[..., 3:]
                alpha_3ch = np.repeat(alpha, 3, axis=2)
                combined = np.concatenate((rgb, alpha_3ch), axis=1)
                frames_rgb.append(combined)

            output_clip = ImageSequenceClip(frames_rgb, fps=fps)
            output_clip = output_clip.set_audio(audio_clip)
            output_clip.write_videofile(output_video_path, codec="libx264", bitrate="20000k", fps=fps)

        else:
            composite_clip = composite_clip.set_audio(audio_clip)
            # Save the composite video file
            composite_clip.write_videofile(output_video_path,
                                        codec='libx264',
                                        bitrate="20000k",
                                        fps=fps)
        
        # clear the temple files
        self.delete_all_files_in_folder(foreground_dir)


