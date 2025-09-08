import os
import shutil


def check_and_move_pairs(folder_path):
    # 支持的图片扩展名
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]

    # 支持的标签扩展名（根据你的描述，标签文件是.txt）
    label_extension = ".txt"

    # 获取文件夹内所有文件
    files = os.listdir(folder_path)

    # 分离图片和标签文件
    image_files = []
    label_files = []

    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext.lower() in image_extensions:
            image_files.append(filename)
        elif ext.lower() == label_extension:
            label_files.append(filename)

    # 找出配对的文件对
    paired_files = []
    unmatched_images = []
    unmatched_labels = []

    # 首先找出所有配对的文件对
    for image_file in image_files:
        # 获取图片文件的基名（不带扩展名）
        image_name = os.path.splitext(image_file)[0]

        # 查找是否有对应的标签文件
        label_file = image_name + label_extension
        if label_file in label_files:
            paired_files.append((image_file, label_file))
            # 从标签文件列表中移除已配对的文件，避免重复配对
            label_files.remove(label_file)
        else:
            unmatched_images.append(image_file)

    # 剩下的标签文件就是没有配对图片的
    unmatched_labels = label_files

    # 创建目标文件夹
    images_folder = os.path.join(folder_path, "images")
    labels_folder = os.path.join(folder_path, "labels")

    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(labels_folder, exist_ok=True)

    # 移动配对的文件
    for image_file, label_file in paired_files:
        # 源文件路径
        src_image_path = os.path.join(folder_path, image_file)
        src_label_path = os.path.join(folder_path, label_file)

        # 目标文件路径
        dst_image_path = os.path.join(images_folder, image_file)
        dst_label_path = os.path.join(labels_folder, label_file)

        # 移动文件
        shutil.move(src_image_path, dst_image_path)
        shutil.move(src_label_path, dst_label_path)
        print(f"Moved pair: {image_file} -> images/, {label_file} -> labels/")

    # 打印未配对的文件
    if unmatched_images:
        print("\n以下图片文件没有找到对应的标签文件:")
        for image_file in unmatched_images:
            print(image_file)

    if unmatched_labels:
        print("\n以下标签文件没有找到对应的图片文件:")
        for label_file in unmatched_labels:
            print(label_file)

    # 打印统计信息
    print("\n统计信息:")
    print(f"配对成功的文件对: {len(paired_files)} 对")
    print(f"未配对的图片文件: {len(unmatched_images)} 个")
    print(f"未配对的标签文件: {len(unmatched_labels)} 个")


if __name__ == "__main__":
    # 使用示例
    folder_path = "/media/jasonwu/新加卷/datasets/overload"
    check_and_move_pairs(folder_path)
