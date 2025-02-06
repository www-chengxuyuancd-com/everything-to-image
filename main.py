import fitz  # PyMuPDF
import sys
import os
import subprocess

# 配置 OSS Bucket 地址
OSS_BUCKET = "oss://python99/auto_images/static/img/books/"  # 替换为你的 OSS Bucket 地址


def extract_first_page_as_image(pdf_path):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)

    # 获取第一页
    first_page = pdf_document.load_page(0)

    # 将第一页转换为图片（PNG格式）
    pix = first_page.get_pixmap()

    # 生成输出图片的文件名
    output_image_name = os.path.splitext(os.path.basename(pdf_path))[0] + "-1.png"
    output_image_path = os.path.join(os.path.dirname(pdf_path), output_image_name)

    # 保存图片
    pix.save(output_image_path)

    print(f"第一页已保存为: {output_image_path}")
    return output_image_path


def upload_to_oss(local_file_path, oss_bucket):
    # 添加 -f 选项以强制覆盖同名文件
    command = f'ossutil cp -f "{local_file_path}" {oss_bucket}'
    print(f"Executing command: {command}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(f"Return code: {result.returncode}")
    print(f"Standard Output: {result.stdout}")
    print(f"Error Output: {result.stderr}")

    if result.returncode == 0:
        # 构造可以访问的链接
        bucket_name = oss_bucket.split("://")[1].split("/")[0]  # 提取 Bucket 名称
        object_path = os.path.join("auto_images/static/img/books/", os.path.basename(local_file_path))
        access_link = f"http://{bucket_name}.oss-cn-beijing.aliyuncs.com/{object_path}"  # 替换 <your_endpoint> 为你的 OSS endpoint
        print(f"文件已成功上传到 OSS: {oss_bucket}")
        print(f"可以访问的链接: {access_link}")
    else:
        print(f"上传失败: {result.stderr}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("请提供PDF文件路径作为参数。")
    else:
        pdf_path = sys.argv[1]
        if os.path.isfile(pdf_path) and pdf_path.lower().endswith('.pdf'):
            image_path = extract_first_page_as_image(pdf_path)
            upload_to_oss(image_path, OSS_BUCKET)
        else:
            print("提供的路径不是一个有效的PDF文件。")