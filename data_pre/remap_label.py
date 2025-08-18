from pathlib import Path


def remap_labels_inplace(data_dir, class_mapping):
    """
    date:2025.7.5
    author:jasonwu
    直接在原目录下修改标签文件，进行类别映射
    参数:
        data_dir (str): 包含图片和标签的目录路径
        class_mapping (dict): 类别映射字典 {原类别: 新类别}.
    """
    data_path = Path(data_dir)
    processed_count = 0
    error_count = 0

    # 遍历目录下所有txt文件（标签文件）
    for label_file in data_path.glob("*.txt"):
        try:
            # 读取原标签内容
            with open(label_file, encoding="utf-8") as f:
                lines = f.readlines()

            # 处理每一行
            new_lines = []
            for line in lines:
                line = line.strip()
                if not line:  # 保留空行
                    new_lines.append(line + "\n")
                    continue

                parts = line.split()
                if len(parts) < 5:  # 跳过不符合YOLO格式的行
                    error_count += 1
                    continue

                # 替换类别ID
                old_class = parts[0]
                new_class = class_mapping.get(old_class)
                if new_class is None:
                    error_count += 1
                    continue

                new_line = f"{new_class} {' '.join(parts[1:])}\n"
                new_lines.append(new_line)

            # 直接覆盖原文件
            with open(label_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            processed_count += 1

        except Exception as e:
            print(f"处理文件 {label_file.name} 时出错: {str(e)}")
            error_count += 1

    print(f"\n处理完成！\n成功处理: {processed_count} 个文件\n错误数量: {error_count}")


if __name__ == "__main__":
    # 配置参数
    DATA_DIR = "1wlabels"

    # 类别映射规则（原类别 -> 新类别）
    CLASS_MAPPING = {
        "0": "0",
        "2": "0",
        "3": "0",
        "5": "0",  # nohelmet -> 0
        "1": "1",
        "4": "1",
        "8": "1",  # normal -> 1
        "6": "2",
        "7": "2",  # overload -> 2
        "9": "3",  # car -> 3
        "10": "4",  # head -> 4
    }

    # CLASS_MAPPING = {
    #     "0": "0",
    #     "2": "1",
    #     "5": "2",
    #     "1": "3",  # nohelmet -> 0
    #     "3": "4",
    #     "4": "5",
    #     "6": "6",  # normal -> 1
    #     "9": "7",
    #     "10": "8",  # overload -> 2
    #     "7": "9",  # car -> 3
    #     "8": "10",  # head -> 4
    # }

    # 执行映射
    remap_labels_inplace(DATA_DIR, CLASS_MAPPING)
