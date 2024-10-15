import os
import tyro
import subprocess
import os.path as osp
from src.gradio_pipeline import GradioPipeline
from src.config.crop_config import CropConfig
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig

class LivePortrait:
    def __init__(self, source_video_path, driving_video_path):
        self.source_video_path = source_video_path
        self.driving_video_path = driving_video_path
    
    def partial_fields(self, target_class, kwargs):
        return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})

    def fast_check_ffmpeg(self):
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except:
            return False
        
    def execute_output(self):
        
        # set tyro theme
        tyro.extras.set_accent_color("bright_cyan")
        args = tyro.cli(ArgumentConfig)

        ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
        if osp.exists(ffmpeg_dir):
            os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

        if not self.fast_check_ffmpeg():
            raise ImportError(
                "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
        )

        # specify configs for inference
        inference_cfg = self.partial_fields(InferenceConfig, args.__dict__)  # use attribute of args to initial InferenceConfig
        crop_cfg = self.partial_fields(CropConfig, args.__dict__)  # use attribute of args to initial CropConfig
        # global_tab_selection = None

        gradio_pipeline = GradioPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg,
        args=args
        )

        output_video_i2v_path, output_video_concat_i2v_path = gradio_pipeline.execute_video(
                                                                                input_source_video_path = self.source_video_path,
                                                                                input_driving_video_path = self.driving_video_path,
                                                                                flag_relative_input=True,
                                                                                flag_do_crop_input=True,
                                                                                flag_remap_input=True,
                                                                                flag_stitching_input=True,
                                                                                driving_option_input="expression-friendly",
                                                                                driving_multiplier=1.0,
                                                                                flag_crop_driving_video_input=False,
                                                                                flag_video_editing_head_rotation=False,
                                                                                scale=2.3,
                                                                                vx_ratio=0.0,
                                                                                vy_ratio=-0.125,
                                                                                scale_crop_driving_video=2.2,
                                                                                vx_ratio_crop_driving_video=0.0,
                                                                                vy_ratio_crop_driving_video=-0.1,
                                                                                driving_smooth_observation_variance=3e-7,
                                                                                tab_selection='Video',
                                                                                v_tab_selection='Video')

        return output_video_i2v_path, output_video_concat_i2v_path