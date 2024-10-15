from infer_audio2vid_acc import EchoMimic_LivePortrait
import torch

def main():
    ref_vid_path = "./assets/driven_video/lianxiang_girl_20s.mov"
    audio_path = "./assets/test_audios/zhengjiuzhe_2.WAV"
    video_save_path = "modified_video_vscode.mp4"
    background_path = "./static/source_backgroud/wukong.jpg"
    scale = 0.75
    position = [-20,400]

    echomimic_live = EchoMimic_LivePortrait(ref_vid_path, audio_path, video_save_path, background_path, scale, position)
    echomimic_live.main()
    
if __name__ == "__main__":
    main()
