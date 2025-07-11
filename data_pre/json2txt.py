import os
import json
from collections import defaultdict

def convert_labelme_to_yolo(
    json_file_path, txt_file_path, img_width, img_height, class_mapping
):
    """
    将LabelMe格式的JSON转换为YOLO格式的TXT
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        shapes = data.get("shapes", [])
        with open(txt_file_path, "w", encoding="utf-8") as f:
            for shape in shapes:
                label = shape.get("label", "")
                if label not in class_mapping:
                    continue  # 跳过不需要的类别

                # 获取矩形坐标（LabelMe格式是[[x1,y1],[x2,y2]]）
                points = shape.get("points", [])
                if len(points) != 2 or shape.get("shape_type") != "rectangle":
                    continue

                # 转换为YOLO格式（中心点坐标和宽高，归一化）
                x1, y1 = points[0]
                x2, y2 = points[1]

                # 确保坐标顺序正确
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])

                # 计算中心点和宽高（归一化）
                x_center = ((x1 + x2) / 2) / img_width
                y_center = ((y1 + y2) / 2) / img_height
                width = (x2 - x1) / img_width
                height = (y2 - y1) / img_height

                # 写入TXT文件
                f.write(
                    f"{class_mapping[label]} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
                )

        return True
    except Exception as e:
        print(f"Error converting {json_file_path}: {str(e)}")
        return False


def process_folder(folder_path, class_mapping):
    """
    处理整个文件夹:
    1. 转换JSON到TXT（YOLO格式）
    2. 统计标签数量
    3. 保留所有图片（不再删除）
    """
    label_stats = defaultdict(int)

    # 获取所有JSON文件
    json_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".json")]
    total_files = len(json_files)
    print(f"Found {total_files} JSON files to process")

    for json_file in json_files:
        base_name = os.path.splitext(json_file)[0]
        json_path = os.path.join(folder_path, json_file)
        txt_path = os.path.join(folder_path, f"{base_name}.txt")

        # 从JSON中获取图片尺寸（需要先读取JSON）
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                img_height = data.get("imageHeight", 0)
                img_width = data.get("imageWidth", 0)
                if img_height == 0 or img_width == 0:
                    print(f"Warning: {json_file} missing image dimensions, skipping")
                    continue
        except:
            print(f"Error reading {json_file}, skipping")
            continue

        # 转换标签
        success = convert_labelme_to_yolo(json_path, txt_path, img_width, img_height, class_mapping)

        if success:
            # 统计标签数量
            if os.path.exists(txt_path):
                with open(txt_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        class_id = line.split()[0]
                        label_stats[class_id] += 1

    # 打印统计信息
    print("\nLabel Statistics:")
    for class_id in sorted(class_mapping.values()):
        class_name = [k for k, v in class_mapping.items() if v == class_id][0]
        count = label_stats.get(class_id, 0)
        print(f"{class_id} ({class_name}): {count}")

    total_labels = sum(label_stats.values())
    print(f"\nTotal labels: {total_labels}")
    print("All original images are preserved")


if __name__ == "__main__":

    class_mapping = {
        "Nohelmet": "0",
        "normal": "1",
        "overload": "2",
        "car": "3",
        "head": "4",
    }
    folder_path = "/media/jasonwu/新加卷/datasets/qijiang_final/others/quarter_2_json"

    process_folder(folder_path, class_mapping)
