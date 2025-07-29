from PIL import Image, ImageEnhance
import numpy as np

def adjust_contrast_highlights_shadows(image_path, shadow_adjust=+20, highlight_adjust=-20):
"""
高光-20  阴影+20
"""
    # 1. 基础对比度调整
    img = Image.open(image_path).convert('RGB')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)  # 全局对比度提升20%

    # 2. 转换为numpy数组操作
    arr = np.array(img).astype(np.int16)  # 使用int16避免溢出

    # 3. 定义亮度阈值范围（可自定义调整）
    shadow_threshold = 80    # 阴影阈值（0-255）
    highlight_threshold = 200 # 高光阈值

    # 4. 阴影区域处理（亮度+20）
    shadow_mask = np.mean(arr, axis=2) < shadow_threshold
    arr[shadow_mask] = np.clip(arr[shadow_mask] + shadow_adjust, 0, 255)

    # 5. 高光区域处理（亮度-20）
    highlight_mask = np.mean(arr, axis=2) > highlight_threshold
    arr[highlight_mask] = np.clip(arr[highlight_mask] + highlight_adjust, 0, 255)

    # 6. 转换回Pillow图像并返回
    return Image.fromarray(arr.astype(np.uint8))

# 调用示例
adjusted_img = adjust_contrast_highlights_shadows("input.jpg")
adjusted_img.save("output.jpg")
