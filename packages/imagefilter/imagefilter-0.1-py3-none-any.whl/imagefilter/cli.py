# 安装库（需先执行）
# pip install pillow-lut
import os
import math
import multiprocessing
from pathlib import Path
import argparse
from imagefilter.enhence import *
from imagefilter.raw import read_image
from imagefilter.luts_adapter import get_adjust_by_lut_name, get_all_luts, LUT
import piexif
from imagefilter.mytypes import Parameter


def process_img(item):
    (img_file, output_file, lut, param) = item
    # 执行处理
    img = read_image(img_file)
    if lut.Color3DLUT:
        print(f"[{img_file}] -> [{output_file}] LUT [{lut.name}] Applying")
        if param.is_default():
            adjust = get_adjust_by_lut_name(img_file, lut.name)
            param = Parameter(adjust[0], adjust[1],adjust[2])
        img = enhance(img_file, img, param)
        img = img.filter(lut.Color3DLUT)

    # 自动色阶
    #img = auto_levels(img)

    # 读取源文件中exif信息
    exif_dict = None
    with open(img_file, 'rb') as f:
        raw_data = f.read()
        exif_dict = piexif.load(raw_data)

    if exif_dict is None:
        img.save(output_file, quality=95)
    else:
        try:
            img.save(output_file, quality=95, exif=piexif.dump(exif_dict))
        except Exception:
            img.save(output_file, quality=95)
    print(f"[{img_file}] -> [{output_file}] saved")

def process_dir(input_path:str, output_path:str, lut:LUT, param:Parameter):
    all_items = []
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for x in Path(input_path).rglob("*"):
        if x.is_file() and x.suffix.upper() in [".ARW", ".JPG", ".JPEG", ".PNG"]:
            input_file = x.resolve()
            output_file = f'{os.path.join(output_path, x.stem)}_{lut.name}.jpg'
            all_items.append((input_file.as_posix(), output_file, lut, param))

    process_num = 1
    if multiprocessing.cpu_count() > 2:
        process_num = multiprocessing.cpu_count() -2
    print(f"start to processing {len(all_items)} pictures on {process_num} cpus")
    from tqdm import tqdm
    with multiprocessing.Pool(process_num) as pool:
        pbar = tqdm(total=len(all_items), desc="processing")
        itr = pool.imap(process_img, all_items)
        for result in itr:
            pbar.update()
            pass
        pbar.close()


#def process(input_path:str, output_path:str, lut_name:str, saturation:int):
def process(input_path:str, output_path:str, lut_name:str, param:Parameter):
    p = Path(input_path)
    output = f"{p.stem}{p.suffix}.{lut_name}.JPG"
    if output_path:
        output = output_path

    lut = LUT(lut_name)
    if os.path.isdir(input_path):
        print(f"[{input_path}] -> [{output_path}] LUT [{lut.name}]")
        process_dir(input_path, output_path, lut, param)
    else:
        print(f"[{input_path}] -> [{output}] LUT [{lut.name}]")
        process_img((input_path, output, lut, param))


def get_luts_help() -> str:
    all_luts = get_all_luts()
    help_str = "LUT名或则LUT文件,内置支持:\n" + '\n'.join([f"{d.name}:\t\t{d.description}" for d in all_luts])
    return help_str


def cli_main():
    parser = argparse.ArgumentParser(description="应用LUT滤镜到图像的命令行工具",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # 添加参数规则
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="input.jpg",  # input参数默认值[7](@ref)
        help="输入图像路径（默认：input.jpg）。支持输入目录，输入目录时遍历处理目录中所有文件"
    )
    parser.add_argument(
        "-l", "--lut",
        type=str,
        required=False,
        help=get_luts_help()
    )
    parser.add_argument(
        "-b", "--bright",
        type=float,
        required=False,
        default=1.0,
        help="亮度"
    )
    parser.add_argument(
        "-c", "--contrast",
        type=float,
        required=False,
        default=1.0,
        help="对比度"
    )
    parser.add_argument(
        "-s", "--saturation",
        type=float,
        required=False,
        default=1.0,
        help="饱和度"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,  # output参数默认值[5](@ref)
        help="输出图像路径（默认：output.jpg）"
    )


    args = parser.parse_args()
    p =Parameter(args.bright, args.contrast, args.saturation)
    print(p)
    process(args.input, args.output, args.lut, p)

if __name__ == "__main__":
    cli_main()
