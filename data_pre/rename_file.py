import os


def rename_files_in_folder(folder_path):
    """
    重命名文件夹中同时包含'.txt'和'.xml'的文件名（删除'.xml'部分）.

    参数:
        folder_path (str): 目标文件夹路径

    说明:
        遍历指定文件夹，将所有同时满足以下条件的文件重命名：
        1. 文件扩展名为.txt
        2. 文件名中包含.xml
        重命名规则为删除文件名中的.xml部分

    示例:
        原文件名: example.xml.txt
        新文件名: example.txt
    """
    files = os.listdir(folder_path)

    # 遍历每个文件
    for filename in files:
        # 检查文件是否是.txt文件且包含.xml
        if filename.endswith(".txt") and ".xml" in filename:
            # 构造新的文件名（删除.xml部分）
            new_filename = filename.replace(".xml", "")

            # 获取文件的完整路径
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    # 使用示例
    folder_path = "/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/overload"
    rename_files_in_folder(folder_path)
