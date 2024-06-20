

import os
import shutil
from datetime import datetime
import zipfile

if os.path.exists('./temp'):
    shutil.rmtree('./temp')
os.mkdir('./temp')


def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return timestamp

def list_specific_files_os(directory, extensions):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                print(os.path.join(root, file))
                shutil.copy2(os.path.join(root, file), './temp')


def create_zip(source_directory, output_filename):
    # 确保输出文件名不包含扩展名
    output_filename = str(output_filename).rstrip('.zip')
    shutil.make_archive(output_filename, 'zip', source_directory)

## 拆分ZIP
def split_zip(source_directory, max_size_bytes, output_filename):
    # 创建一个空的zip文件
    zip_filename = output_filename + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        total_size = 0
        part_number = 1
        part_size = 0
        part_filename = f"{output_filename}_part{part_number}.zip"
        part_zipf = zipfile.ZipFile(part_filename, 'w', zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(source_directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                if part_size + file_size > max_size_bytes:
                    print(part_size + file_size,max_size_bytes)
                    part_zipf.close()
                    part_size = 0
                    part_number += 1
                    part_filename = f"{output_filename}_part{part_number}.zip"
                    part_zipf = zipfile.ZipFile(part_filename, 'w', zipfile.ZIP_DEFLATED)

                part_zipf.write(file_path, os.path.relpath(file_path, source_directory))
                part_size += file_size

        part_zipf.close()

    print(f"Split into {part_number} parts.")
    
# 示例调用
nuget_root_path = r'E:\09Nuget'
source_directory = nuget_root_path
output_filename = f"nupkg_{get_timestamp()}"
extensions = ['.nupkg']
list_specific_files_os(source_directory, extensions)
# create_zip('./temp',output_filename) 
max_size_bytes = 100 * 1024 * 1024   # 100 MB 
split_zip('./temp', max_size_bytes, output_filename)