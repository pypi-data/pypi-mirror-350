import subprocess
from pathlib import Path


def b_convert_ts2mp4(input_path: Path | str, output_path: Path | str = None):
    input_path, output_path = Path(input_path), Path(output_path)

    if not str(input_path).endswith('.ts'):
        raise ValueError("输入文件必须是 .ts 格式")

    if output_path is None:
        output_path = str(input_path).replace('.ts', '.mp4')
        output_path = Path(output_path)

    command = [
        'ffmpeg',
        '-i', input_path,  # 输入文件
        '-c', 'copy',  # 拷贝编码，无需重新压缩（快）
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"转换成功：{output_path}")
    except subprocess.CalledProcessError as e:
        print("转换失败：", e)


if __name__ == '__main__':
    # 示例
    b_convert_ts2mp4('./awaaa/21.ts')
