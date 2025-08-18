import os
from pathlib import Path

from ultralytics import YOLO


class ImageLabelProcessor:
    def __init__(self, input_folder, output_folder, model_path):
        """
        图片标签处理类的初始化方法。.

        Args:
            input_folder (str): 输入文件夹路径,包含图片数据
            output_folder (str): 输出文件夹路径,用于存储标签文件
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.model_path = model_path  # 加载YOLO模型

        # 确保输出文件夹存在
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)

    def process_images(self, save):
        """处理输入文件夹中的所有图片，生成对应的标签文件."""
        # 支持的图片格式
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

        # 遍历输入文件夹
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(image_extensions):
                input_path = os.path.join(self.input_folder, filename)
                print(f"正在处理图片: {filename}")

                # 进行目标检测

                model = YOLO(self.model_path)
                results = model.predict(input_path, device="cuda:0", save=save)

                # 生成标签文件路径
                label_filename = os.path.splitext(filename)[0] + ".txt"
                label_path = os.path.join(self.output_folder, label_filename)

                # 保存检测结果为YOLO格式标签
                self._save_coco_labels(results, label_path)
                print(f"已生成标签文件: {label_filename}")

    def _save_coco_labels(self, results, output_path):
        """
        将检测结果保存为COCO/YOLO格式的标签文件.

        Args:
            results: YOLO模型的检测结果
            output_path (str): 标签文件输出路径
        """
        with open(output_path, "w") as f:
            for result in results:
                boxes = result.boxes
                xywhn = boxes.xywhn  # 获取归一化坐标
                cls_ids = boxes.cls  # 获取检测到的类别ID

                for box, cls_id in zip(xywhn, cls_ids):
                    x_center, y_center, width, height = box.tolist()
                    cls_id = int(cls_id.item())  # 将类别ID转换为整数
                    # YOLO格式: class_id x_center y_center width height
                    f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")


if __name__ == "__main__":
    # 用户输入
    input_folder = "/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/qijiang4"
    output_folder = "/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/qijiang4_label"

    # 验证输入文件夹是否存在
    if not os.path.isdir(input_folder):
        print("错误: 指定的图片文件夹不存在!")
        exit(1)

    # 处理图片
    processor = ImageLabelProcessor(input_folder, output_folder)
    processor.process_images()

    print("所有图片处理完成!")
