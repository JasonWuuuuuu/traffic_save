from ultralytics import YOLO
# # import os
# # os.environ['KMP_DUPLICATE_LIB_OK']='True'

model = YOLO('yolo11n.pt')
result = model.predict(source = 0, device = 'cpu', workers = 0, imgsz = 640, show = True)


# import torch

# # 检查 CUDA 是否可用
# print(torch.cuda.is_available()) # 应该返回 True

# # 检查 GPU 数量
# print(torch.cuda.device_count()) # 应该返回你的 GPU 数量