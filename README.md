<h1 align='center'>🌟LianxiangAvatar</h1>

## Updates
- [2025.04.20] ✨Optimize output content
- [2025.02.20] Added an optional branch. When the background image is None, directly output a transparent background video
- [2025.02.12] Added video super-resolution function
- [2024.10.16] Release the first version of lianxiang_avatar


## Installtion
Create conda environment (Recommended):
```bash
  conda create -n echomimic python=3.8
  conda activate echomimic
```

Install packages with `pip`
```bash
  pip install -r requirements.txt
```

### Download pretrained weights
```shell
git lfs install
git clone https://huggingface.co/BadToBest/EchoMimic pretrained_weights
```

The **pretrained_weights** is organized as follows.
```
./pretrained_weights/
├── denoising_unet.pth
├── reference_unet.pth
├── motion_module.pth
├── face_locator.pth
├── sd-vae-ft-mse
│   └── ...
├── sd-image-variations-diffusers
│   └── ...
└── audio_processor
    └── whisper_tiny.pt
```

## SuperResolution Instruction
### Basics
Use the following command to upscale a video by 4x with RealESRGAN:
```
video2x -i input.mp4 -o output.mp4 -f realesrgan -r 4 -m realesr-animevideov3
```
Use the following command to upscale a video to with libplacebo + Anime4Kv4 Mode A+A:
```
video2x -i input.mp4 -o output.mp4 -f libplacebo -s anime4k-v4-a+a -w 3840 -h 2160
```

### Advanced
It is possible to specify custom MPV-compatible GLSL shader files with the --shader, -s argument:
```
video2x -i input.mp4 -o output.mp4 -f libplacebo -s path/to/custom/shader.glsl -w 3840 -h 2160
```
List the available GPUs with --list-gpus, -l:
```
$ video2x --list-gpus
0. NVIDIA RTX A6000
        Type: Discrete GPU
        Vulkan API Version: 1.3.289
        Driver Version: 565.228.64
```
Select which GPU to use with the --gpu, -g argument:
```
video2x -i input.mp4 -o output.mp4 -f realesrgan -r 4 -m realesr-animevideov3 -g 1
```
Specify arbitrary extra FFmpeg encoder options with the --extra-encoder-options, -e argument:
```
video2x -i input.mkv -o output.mkv -f realesrgan -m realesrgan-plus -r 4 -c libx264rgb -e crf=17 -e preset=v
```