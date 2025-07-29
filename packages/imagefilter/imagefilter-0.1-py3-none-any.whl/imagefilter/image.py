# 安装库（需先执行）
# pip install pillow-lut
import os
import rawpy
import argparse
from PIL import Image
from pillow_lut import load_cube_file
from imagefilter.enhence import update_all, update_saturation
from imagefilter.luts_adapter import get_adjust_by_lut_name


def read_to_rgb(image_path):
    image = None
    if not image_path.endswith('ARW'):
        image = Image.open(image_path).convert('RGB')
    else:
        raw = rawpy.imread(image_path)
        rgb = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_color=rawpy.ColorSpace.sRGB,
            demosaic_algorithm=rawpy.DemosaicAlgorithm.AAHD)
        image = Image.fromarray(rgb)
    return image

def apply_lut(image, lut_name):
    if os.path.exists(lut_name):
        lut = load_cube_file(lut_name)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lut = load_cube_file(os.path.join(base_dir, 'luts', f'{lut_name}.cube'))
    return image.filter(lut)

def image_main():
    # 创建解析器并设置程序描述[5](@ref)
    parser = argparse.ArgumentParser(description="应用LUT滤镜到图像的命令行工具")
    # 添加参数规则
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="input.jpg",  # input参数默认值[7](@ref)
        help="输入图像路径（默认：input.jpg）"
    )
    parser.add_argument(
        "-l", "--lut",
        type=str,
        required=False,  # lut参数必须提供[7](@ref)
        help="LUT名"
    )
    parser.add_argument(
        "-s", "--saturation",
        type=float,
        required=False,
        help="饱和度"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,  # output参数默认值[5](@ref)
        help="输出图像路径（默认：output.jpg）"
    )

    # 示例：打印参数值
    args = parser.parse_args()
    print(f"输入文件: {args.input}")
    print(f"LUT文件: {args.lut}")
    output = f"{args.input.split('.')[0]}_{args.lut}.jpg"
    if args.output:
        output = args.output
    print(f"输出文件: {output}")

    # 执行处理
    img = read_to_rgb(args.input)
    #img = dynamic_brightness_adjust(img)
    adjust=get_adjust_by_lut_name(args.input, args.lut)
    img = update_all(img, adjust)

    if args.lut:
        print("applying lut")
        img = apply_lut(img, args.lut)
    if args.saturation:
        print(f"饱和度: {args.saturation}")
        img = update_saturation(img, args.saturation)
    #if args.input.endswith('ARW'):
    #    img = update_all(img, (1.2,1.0,1.1))
    #img = white_balance(img)
    #img = matrix(img)
    img.save(output, quality=95)
    print(f"{output} saved")

if __name__ == "__main__":
    image_main()
