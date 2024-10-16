<h1 align='center'>LianxiangAvatar</h1>
## Updates
- [2024.10.16] release the first version of lianxiang_avatar
## Installtion
Create conda environment (Recommended):
```bash
  conda create -n echomimic python=3.8
  conda activate echomimic
```

Install packages with `pip`
```bash
  pip install -r requirements.txt

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
