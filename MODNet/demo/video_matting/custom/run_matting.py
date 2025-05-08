import os
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from MODNet.src.models.modnet import MODNet

class Modnet:
    def __init__(self, foreground_dir):
        self.foreground_dir = foreground_dir
        print('Load pre-trained MODNet...')
        self.pretrained_ckpt = './MODNet/pretrained/modnet_webcam_portrait_matting.ckpt'
        self.modnet = MODNet(backbone_pretrained=False)
        self.modnet = nn.DataParallel(self.modnet)

        self.GPU = True if torch.cuda.device_count() > 0 else False
        if self.GPU:
            print('Use GPU...')
            self.modnet = self.modnet.cuda()
            self.modnet.load_state_dict(torch.load(self.pretrained_ckpt))
        else:
            print('Use CPU...')
            self.modnet.load_state_dict(torch.load(self.pretrained_ckpt, map_location=torch.device('cpu')))
        self.modnet.eval()

        self.torch_transforms = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )
    
    def gen_video_without_green(self, output_vid_path):
        if not os.path.exists(output_vid_path):
            print('Cannot find the input video: {0}'.format(output_vid_path))
            exit()
        # video capture
        vc = cv2.VideoCapture(output_vid_path)

        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False

        if not rval:
            print('Failed to read the video: {0}'.format(output_vid_path))
            exit()

        num_frame = vc.get(cv2.CAP_PROP_FRAME_COUNT)
        h, w = frame.shape[:2]
        if w >= h:
            rh = 512
            rw = int(w / h * 512)
        else:
            rw = 512
            rh = int(h / w * 512)
        rh = rh - rh % 32
        rw = rw - rw % 32

        print('Start matting...')
        with tqdm(range(int(num_frame)))as t:
            c = 0
            while rval:
                # print(f"Processing frame {c}")
                frame_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_np = cv2.resize(frame_np, (rw, rh), cv2.INTER_AREA)

                frame_PIL = Image.fromarray(frame_np)
                frame_tensor = self.torch_transforms(frame_PIL)
                frame_tensor = frame_tensor[None, :, :, :]
                if self.GPU:
                    frame_tensor = frame_tensor.cuda()

                with torch.no_grad():
                    _, _, matte_tensor = self.modnet(frame_tensor, True)

                matte_tensor = matte_tensor.repeat(1, 3, 1, 1)
                matte_np = matte_tensor[0].data.cpu().numpy().transpose(1, 2, 0)

                # Convert the three-channel image to a grayscale image
                gray_image = cv2.cvtColor(matte_np, cv2.COLOR_BGR2GRAY)
                kernel = np.ones((5, 5), np.uint8)  # 5x5 square structuring element
                # Perform erosion
                eroded_image = cv2.erode(gray_image, kernel, iterations=1)
                # If you want to convert the result back to a three-channel image
                dilated_image_3ch = np.stack([eroded_image]*3, axis=-1)

                alpha_channel = (dilated_image_3ch * 255).astype(np.uint8)

                rgba_image = np.dstack((frame_np, alpha_channel[:, :, 0]))
                rgba_image = cv2.resize(rgba_image, (w, h), cv2.INTER_CUBIC)
                
                # save as png sequences
                output_path = os.path.join(self.foreground_dir, f"frame_{c:06d}.png")
                Image.fromarray(rgba_image).save(output_path)
                # read next frame
                rval, frame = vc.read()
                c += 1
                t.update(1)