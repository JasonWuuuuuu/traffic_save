import os

def count_labels_in_voc_format_txt_files(folder_path):
    label_counts = {}
    
    # 获取文件夹内所有文件
    files = os.listdir(folder_path)
    
    # 遍历每个文件
    for filename in files:
        # 只处理.txt文件
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                # 统计每个标签（假设每行第一个元素是类别名称）
                for line in lines:
                    parts = line.strip().split()  # 按空白字符分割
                    if parts:  # 忽略空行
                        label = parts[0]  # 第一个元素是类别名称
                        if label in label_counts:
                            label_counts[label] += 1
                        else:
                            label_counts[label] = 1
    
    # 打印统计结果
    print("标签统计结果:")
    for label, count in sorted(label_counts.items()):
        print(f"{label}: {count}次")

if __name__ == "__main__":

    # 使用示例
    folder_path = '/media/jasonwu/新加卷/datasets/qijiang_final/qijiang/qijiang4_label'
    count_labels_in_voc_format_txt_files(folder_path)