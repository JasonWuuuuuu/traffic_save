import os
from pathlib import Path


def rename_dataset_files(root_dir):
    """
    重命名已整理的数据集文件，按照顺序编号（1,2,3...），保持图片和标签对应
    参数:
        root_dir (str): 已整理的数据集根目录.
    """
    base_path = Path(root_dir)

    # 定义要处理的子目录
    splits = ["train", "val", "test"]

    for split in splits:
        print(f"正在处理 {split} 集...")

        # 获取图片和标签路径
        img_dir = base_path / "images" / split
        label_dir = base_path / "labels" / split

        # 获取所有图片文件并按当前名称排序（确保一致性）
        img_files = sorted(os.listdir(img_dir))

        # 为每个文件分配新名称
        for idx, img_file in enumerate(img_files, start=1):
            # 获取文件扩展名
            img_ext = os.path.splitext(img_file)[1]
            label_ext = ".txt"

            # 构建旧标签文件名（基于图片旧名称）
            old_label_name = os.path.splitext(img_file)[0] + label_ext

            # 新文件名
            new_base_name = str(idx)
            new_img_name = new_base_name + img_ext
            new_label_name = new_base_name + label_ext

            # 旧文件完整路径
            old_img_path = img_dir / img_file
            old_label_path = label_dir / old_label_name

            # 新文件完整路径
            new_img_path = img_dir / new_img_name
            new_label_path = label_dir / new_label_name

            # 重命名图片文件
            if old_img_path.exists():
                os.rename(old_img_path, new_img_path)

            # 重命名对应的标签文件（如果存在）
            if old_label_path.exists():
                os.rename(old_label_path, new_label_path)
            else:
                print(f"警告: 找不到与 {img_file} 对应的标签文件")

    print("""
    文件重命名完成！
    所有图片和标签文件已按顺序编号（1.jpg, 1.txt, 2.jpg, 2.txt...）
    保持了原有的train/val/test划分结构
    """)


if __name__ == "__main__":
    # 配置您的已整理数据集路径
    ORGANIZED_DATASET_ROOT = "/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/qijiang_all"

    # 执行重命名
    rename_dataset_files(ORGANIZED_DATASET_ROOT)
