import os
import shutil
from pathlib import Path

def find_and_copy_images_flat(source_dir, target_dir, image_extensions=None):
    """
    递归查找源目录中的所有图片文件，并将它们直接复制到目标目录（不保留文件夹结构）
    
    参数:
        source_dir: 要搜索的源目录路径
        target_dir: 保存图片的目标目录路径
        image_extensions: 要查找的图片扩展名列表(不区分大小写)
    """
    if image_extensions is None:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # 创建目标目录(如果不存在)
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # 用于跟踪文件名，避免重复
    name_counter = {}
    
    # 遍历源目录及其所有子目录
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            # 检查文件扩展名是否在图片扩展名列表中
            if file_path.suffix.lower() in image_extensions:
                try:
                    # 处理可能的重名文件
                    dest_name = file
                    while (Path(target_dir) / dest_name).exists():
                        name, ext = os.path.splitext(file)
                        # 在文件名后添加数字 (1), (2), ...
                        if name not in name_counter:
                            name_counter[name] = 1
                        else:
                            name_counter[name] += 1
                        dest_name = f"{name}({name_counter[name]}){ext}"
                    
                    # 构造目标路径
                    dest_path = Path(target_dir) / dest_name
                    # 复制文件
                    shutil.copy2(file_path, dest_path)
                    print(f"已复制: {file_path} -> {dest_path}")
                except Exception as e:
                    print(f"复制文件 {file_path} 时出错: {e}")

if __name__ == "__main__":
    # 用户输入源文件夹路径
    source_folder = 'vehicle20250703'
    
    # 验证源文件夹是否存在
    if not os.path.isdir(source_folder):
        print("错误: 指定的文件夹不存在!")
        exit(1)
    
    # 设置目标文件夹(在源文件夹同级目录下创建"CollectedImages_Flat")
    target_folder = os.path.join(os.path.dirname(source_folder), "qijiang4")
    
    # 执行查找和复制操作
    print(f"开始从 {source_folder} 查找图片...")
    print(f"图片将被复制到 {target_folder}（不保留文件夹结构）")
    
    find_and_copy_images_flat(source_folder, target_folder)
    
    print("操作完成!")