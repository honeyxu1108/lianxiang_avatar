# from PIL import Image

# # 读取图像
# image = Image.open('/home/xf/lianxiang_digital/MODNet/outdir/frame_000000.png')

# # 转换为NumPy数组以获取形状
# import numpy as np
# image_array = np.array(image)

# # 显示图像形状
# print("图像形状 (高度, 宽度, 通道数):", image_array.shape)

# import cv2

# # 读取图像（包括alpha通道）
# image = cv2.imread('/home/xf/lianxiang_digital/MODNet/outdir/frame_000000.png', cv2.IMREAD_UNCHANGED)

# # 显示图像形状
# print("图像形状 (高度, 宽度, 通道数):", image.shape)


import cv2
import imageio
import os
import numpy as np

# 设置PNG图片序列的路径
image_folder = '/home/xf/lianxiang_digital/MODNet/outdir'  # 替换为你的PNG图片序列文件夹路径
output_video = 'output_video_with_alpha.mov'  # 输出视频文件名

# 获取所有PNG文件并按文件名排序
images = [img for img in os.listdir(image_folder) if img.endswith('.png')]
images.sort()  # 确保按顺序读取

# 读取第一张图片以获取尺寸
first_image = cv2.imread(os.path.join(image_folder, images[0]), cv2.IMREAD_UNCHANGED)
height, width, channels = first_image.shape

# 设置视频帧率（FPS）
fps = 30  # 根据需要调整

# 使用imageio创建视频写入器
# with imageio.get_writer(output_video, fps=fps, codec='qtrle', format='mov', pixelformat='argb') as writer:
#     for i, image_name in enumerate(images):
#         # 读取每张图片（包括alpha通道）
#         image_path = os.path.join(image_folder, image_name)
#         image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
#         print(f"{i}图像形状 (高度, 宽度, 通道数):{image.shape}")
#         if image is None:
#             print(f"无法读取图像: {image_path}")
#             continue  # 跳过损坏的文件

#         # 将BGR格式转换为RGBA格式（imageio需要RGBA）
#         rgba_image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

#         # 将图像添加到视频中
#         writer.append_data(rgba_image)

with imageio.get_writer(output_video, fps=fps, codec='qtrle', format='mov', pixelformat='argb') as writer:
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        print("图像形状 (高度, 宽度, 通道数):", image.shape)
        if image is None:
            print(f"无法读取图像: {image_path}")
            continue
        rgba_image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        writer.append_data(rgba_image)

print(f"视频已保存为: {output_video}")