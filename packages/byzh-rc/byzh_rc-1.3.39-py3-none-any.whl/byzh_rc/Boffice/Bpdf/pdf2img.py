try:
    from pdf2image import convert_from_path
except:
    raise ImportError("[PDF to PNG] 请先安装pdf2image库: pip install pdf2image")

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def b_pdf2img(pdf_path, output_dir, format='png', dpi=200, cpu_use:int = None):
    '''
    :param pdf_path:
    :param output_dir:
    :param format: png, jpg, ...
    :param dpi: 越高越清晰
    :param cpu_use: 采用核心数(不指定则采用总核心的四分之一)
    :return:
    '''
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    pdf_name = pdf_path.stem
    if not pdf_path.is_file():
        print(f"路径 {pdf_path} 无法访问")
    os.makedirs(output_dir, exist_ok=True)

    cpu_count = os.cpu_count()
    if cpu_use is None:
        cpu_use = int(cpu_count / 4)
    print(f"[PDF to PNG] 当前CPU核心数{cpu_count}, 采用{cpu_use}个核心")
    print("[PDF to PNG] 正在处理数据中: ")
    images = convert_from_path(pdf_path, dpi=dpi, thread_count=cpu_use)

    def save_image(index, image):
        image.save(output_dir / f"{pdf_name}_{index + 1}.{format}", format.upper())

    with ThreadPoolExecutor() as executor:
        executor.map(save_image, range(len(images)), images)

    print(f"[PDF to PNG] {len(images)} 张 {format.upper()} 图片已保存至路径 {output_dir}")

if __name__ == "__main__":
    pdf_path = "./数据结构与算法.pdf"
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)
    b_pdf2img(pdf_path, output_folder)