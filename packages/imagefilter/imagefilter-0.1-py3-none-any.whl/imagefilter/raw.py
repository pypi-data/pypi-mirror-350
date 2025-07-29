import rawpy
import numpy as np
from PIL import Image, ImageEnhance

import numpy as np
from PIL import Image

    # Step 1: 去除sRGB伽马校正（转换为线性RGB）
def inverse_gamma(u):
    mask = u <= 0.04045
    return np.where(mask, u / 12.92, ((u + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(linear_rgb):
    """
    将线性RGB转换为伽马编码的sRGB
    :param linear_rgb: 输入线性RGB数组（范围[0.0, 1.0]，float32类型）
    :return: sRGB数组（uint8类型，范围0-255）
    """
    # 确保输入在合法范围内
    linear_rgb = np.clip(linear_rgb, 0.0, 1.0)

    # 应用伽马编码
    mask = linear_rgb <= 0.0031308
    srgb_normalized = np.where(
        mask,
        12.92 * linear_rgb,
        1.055 * (linear_rgb ** (1/2.4)) - 0.055
    )

    # 转换为0-255整数并截断溢出
    srgb_uint8 = (np.clip(srgb_normalized, 0.0, 1.0) * 255).astype(np.uint8)
    return srgb_uint8

def reinhard_tone_mapping(img, a=0.18, gamma=2.2):
    """
    Reinhard色调映射算法实现
    :param input_path: 输入HDR图像路径（需为浮点型数据，例如.exr格式）
    :param output_path: 输出LDR图像路径
    :param a: 关键值（默认0.18，控制中灰色调）
    :param gamma: 伽马校正值（默认2.2）
    """
    # 读取图像并转换为浮点型数组 (HDR)
    #img = Image.open(input_path)
    img_array = np.array(img).astype(np.float32) / 255.0  # 归一化到[0, 1]
    img_array = inverse_gamma(img_array)

    # RGB转XYZ颜色空间（提取亮度Y通道）
    """
    rgb_to_xyz = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9504041]
    ])
    """
    rgb_to_xyz = np.array([
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9504]
    ])
    xyz = np.dot(img_array, rgb_to_xyz.T)
    L_w = xyz[..., 1]  # 提取Y通道（亮度）

    # 计算对数平均亮度（避免除零）
    epsilon = 1e-6
    L_w_avg = np.exp(np.mean(np.log(L_w + epsilon)))

    # 缩放亮度通道
    L = (a / L_w_avg) * L_w

    # Reinhard全局压缩公式：L_d = L / (1 + L)
    L_compressed = L / (1 + L)

    # 恢复颜色并转换回RGB
    xyz[..., 1] = L_compressed  # 替换压缩后的Y通道
    xyz_to_rgb = np.linalg.inv(rgb_to_xyz)
    rgb_compressed = np.clip(np.dot(xyz, xyz_to_rgb.T), 0, 1)

    # 伽马校正（模拟显示设备的非线性响应）
    #rgb_gamma = np.power(rgb_compressed, 1/gamma)

    # 转换为8位图像并保存
    #output_array = (rgb_gamma * 255).astype(np.uint8)
    output_array = linear_to_srgb(rgb_compressed)
    print("============================================")
    return Image.fromarray(output_array)

def read_arw(file_path:str):
    """
    for sony ARW
    TODO: 镜头畸变修正
    """
    print(f"[{file_path}] Decoding raw")
    raw = rawpy.imread(file_path)
    rgb = raw.postprocess(
        use_camera_wb=True,
        no_auto_bright=False,
        output_bps=8,
        output_color=rawpy.ColorSpace.Adobe,
        fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode.Full,
        demosaic_algorithm=rawpy.DemosaicAlgorithm.AAHD)

    return Image.fromarray(rgb)

def read_image(file_path:str):
    if file_path.__str__().endswith('ARW'):
        return read_arw(file_path)
    else:
        return Image.open(file_path).convert('RGB')
