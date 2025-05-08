from infer_audio2vid_acc import EchoMimic_LivePortrait
import torch

def main():
    ref_vid_path = "./assets/driven_video/lianxiang_demo_24fps.mp4"
    audio_path = "./assets/test_audios/output.WAV"
    video_save_path = "modified_video_vscode.mp4"
    # background_path = "./static/source_backgroud/lianxiang.jpg"
    background_path = None
    scale = 0.5
    position = [-20,200]
    sp = True

    echomimic_live = EchoMimic_LivePortrait(ref_vid_path, audio_path, video_save_path, background_path, scale, position, sp)
    echomimic_live.main()
    
if __name__ == "__main__":
    main()