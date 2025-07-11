import os
import random
import shutil
from pathlib import Path


def organize_dataset(root_dir, train_value = 0.8, val_value = 0.1):
    '''
    date:2025.7.5
    author:jasonwu
    input:
    root_dir:(str)
    train_value:(float)
    val_value:(float)
    按照8：1：1划分数据集
    '''
    # 创建目标文件夹结构
    base_path = Path(root_dir)
    for folder in [
        "images/train",
        "images/val",
        "images/test",
        "labels/train",
        "labels/val",
        "labels/test",
    ]:
        (base_path / folder).mkdir(parents=True, exist_ok=True)

    # 获取所有图片文件（不包含子目录）
    img_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    image_files = [
        f
        for f in os.listdir(root_dir)
        if os.path.splitext(f)[1].lower() in img_extensions
    ]

    # 获取所有标签文件（不包含子目录）
    label_files = [f for f in os.listdir(root_dir) if f.lower().endswith(".txt")]

    # 建立图片和标签的对应关系（通过文件名）
    paired_files = []
    for img in image_files:
        base_name = os.path.splitext(img)[0]
        matching_labels = [
            l for l in label_files if os.path.splitext(l)[0] == base_name
        ]
        if matching_labels:
            paired_files.append((img, matching_labels[0]))

    # 随机打乱并分割数据集（8:1:1比例）
    random.shuffle(paired_files)
    total = len(paired_files)
    train_end = int(train_value * total)
    val_end = train_end + int(val_value * total)

    # 移动文件到对应目录
    for i, (img_file, label_file) in enumerate(paired_files):
        if i < train_end:
            dest = "train"
        elif i < val_end:
            dest = "val"
        else:
            dest = "test"

        # 移动图片
        shutil.move(
            str(base_path / img_file), str(base_path / "images" / dest / img_file)
        )

        # 移动标签
        shutil.move(
            str(base_path / label_file), str(base_path / "labels" / dest / label_file)
        )

    print(
        f"""
    数据集整理完成！
    总文件对: {total}
    训练集: {train_end} 对
    验证集: {val_end - train_end} 对
    测试集: {total - val_end} 对
    
    最终目录结构:
    {root_dir}
    ├── images
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── labels
        ├── train/
        ├── val/
        └── test/
    """
    )


if __name__ == "__main__":
    # 配置您的数据集路径
    DATASET_ROOT = "/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/qijiang_all"

    # 执行整理
    organize_dataset(DATASET_ROOT)
