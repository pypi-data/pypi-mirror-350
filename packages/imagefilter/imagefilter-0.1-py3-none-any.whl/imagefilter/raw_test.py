import rawpy
import sys
import numpy as np
from PIL import Image, ImageEnhance

def convert_arw_to_jpg(arw_path, jpg_path, gamma=2.2, brightness=1.2, contrast=1.1):
    # 读取ARW原始数据
    with rawpy.imread(arw_path) as raw:
        # 关键参数设置（解决偏暗问题）
        rgb = raw.postprocess(
            use_camera_wb=True,       # 启用相机白平衡[1](@ref)
            no_auto_bright=False,      # 允许自动亮度调整[1](@ref)
            output_bps=8,             # 输出8bit数据
            output_color=rawpy.ColorSpace.Adobe,
            gamma=(gamma, gamma),     # 自定义Gamma校正[7](@ref)
            demosaic_algorithm=rawpy.DemosaicAlgorithm.AAHD  # 高质量去马赛克
        )
    
    # 转换为PIL Image对象
    pil_img = Image.fromarray(rgb)
    
    # 亮度/对比度增强（可选）
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(brightness)
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(contrast)
    
    # 保存JPG（质量参数控制压缩率）
    pil_img.save(jpg_path, quality=95, subsampling=0)

    
def smart_brightness_adjust(rgb_array, max_target=230):
    """
    智能亮度调整算法
    max_target: 允许的最大像素值（防止过曝）
    """
    # 转换为YUV色彩空间处理亮度通道
    yuv = np.array(Image.fromarray(rgb_array).convert('YCbCr'))
    y = yuv[:,:,0].astype(float)
    
    # 计算当前亮度分布
    hist, bins = np.histogram(y, bins=256, range=(0,255))
    current_max = np.percentile(y, 99.9)  # 取99.9%分位数作为有效最大值
    
    # 动态调整参数
    if current_max < 100:  # 极暗场景
        scale_factor = (max_target - 10) / current_max
        gamma = 2.5
    else:
        scale_factor = max_target / current_max
        gamma = 2.3
    
    # 非线性亮度变换
    y = np.clip((y / 255) ** gamma * 255 * scale_factor, 0, 255)
    
    # 合并回RGB
    yuv[:,:,0] = y.astype(np.uint8)
    return np.array(Image.fromarray(yuv, 'YCbCr').convert('RGB'))

def convert_arw_safely(arw_path, output_path):
    with rawpy.imread(arw_path) as raw:
        # 初始解码参数（保留更多高光细节）
        rgb = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=False,
            output_color=rawpy.ColorSpace.sRGB,
            output_bps=8,  # 使用16bit保留更多信息
            #highlight_mode=rawpy.HighlightMode.Clip  # 高光剪切模式
            fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode.Full,
            bright=1.0,
            demosaic_algorithm=rawpy.DemosaicAlgorithm.AAHD
        )
    
    # 转换到PIL并应用智能调整
    pil_img = Image.fromarray(rgb)
    rgb_array = np.array(pil_img)
    
    # 分通道处理防止色偏
    adjusted = smart_brightness_adjust(rgb_array)
    
    # 对比度优化
    enhancer = ImageEnhance.Contrast(Image.fromarray(adjusted))
    final_img = enhancer.enhance(1.1)
    
    # 保存时检查过曝区域
    final_array = np.array(final_img)
    overexposed = np.mean(final_array > 250)
    if overexposed > 0.01:  # 如果过曝区域超过1%
        final_array = np.where(final_array > 250, 250, final_array)
    
    Image.fromarray(final_array).save(output_path, quality=95)

# 使用示例
convert_arw_to_jpg(sys.argv[1], 'output1.jpg', gamma=2.5, brightness=1.8, contrast=1.0)
convert_arw_safely(sys.argv[1], 'output2.jpg')