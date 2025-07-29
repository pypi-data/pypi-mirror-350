import math
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from imagefilter.mytypes import Parameter


def enhance(img_file:str, img:Image.Image, args:Parameter) -> Image.Image:
    """
    更新亮度、对比度、和饱和度
    """
    #(bright, contrast, color) = args
    temp = get_image_color_temp(img)
    print(f"[{img_file}] 色温:{temp} 亮度:{args.bright} 对比度:{args.contrast} 饱和度:{args.saturation} {img.mode}")
    if not math.isclose(args.bright, 1.0):
        img = ImageEnhance.Brightness(img).enhance(args.bright)
    if not math.isclose(args.contrast, 1.0):
        img = ImageEnhance.Contrast(img).enhance(args.contrast)
    if not math.isclose(args.saturation, 1.0):
        img = ImageEnhance.Color(img).enhance(args.saturation)
    return img

def update_saturation(img, value):
    if math.isclose(value, 1.0):
        return img
    print(f"饱和度: {value}")
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(value)

def auto_white_balance(img):
    r, g, b = img.split()
    avg_r = sum(r.getdata()) / (r.width * r.height)
    avg_g = sum(g.getdata()) / (g.width * g.height)
    avg_b = sum(b.getdata()) / (b.width * b.height)
    # 计算调整系数
    scale_r = avg_g / avg_r
    scale_b = avg_g / avg_b
    r = r.point(lambda x: x * scale_r)
    b = b.point(lambda x: x * scale_b)
    balanced_img = Image.merge('RGB', (r, g, b))
    return balanced_img

def estimate_temp(rg_ratio, bg_ratio):
    # 预置色温曲线数据（示例）
    color_temp_curve = {
        2500: (1.35, 0.85),   # (R增益, B增益)
        4500: (1.10, 0.95),
        6500: (0.95, 1.10),
        8500: (0.80, 1.30)
    }
    # 计算与色温曲线的欧式距离
    distances = {
        temp: np.sqrt((rg - rg_ratio)**2 + (bg - bg_ratio)**2)
        for temp, (rg, bg) in color_temp_curve.items()
    }
    return min(distances, key=distances.get)


def get_image_color_temp(img):
    """
    计算色温
    """
    arr = np.array(img) / 255.0
    # 分块处理
    h, w = arr.shape[:2]
    block_size = 25
    valid_blocks = []
    
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = arr[y:y+block_size, x:x+block_size]
            r, g, b = block[...,0], block[...,1], block[...,2]
            
            # 白区检测
            white_mask = (r > 0.7) & (g > 0.7) & (b > 0.7)
            if np.mean(white_mask) < 0.3 or np.mean(white_mask) > 0.7:
                continue
                
            rg_ratio = np.mean(r[white_mask]) / np.mean(g[white_mask])
            bg_ratio = np.mean(b[white_mask]) / np.mean(g[white_mask])
            valid_blocks.append((rg_ratio, bg_ratio))
    
    # 色温估算
    temp_values = [estimate_temp(rg, bg) for rg, bg in valid_blocks]
    return np.median(temp_values)  # 取中值避免异常值

def kelvin_to_rgb(kelvin):
    """McCamy色温公式转换（单位：开尔文）"""
    temp = kelvin / 100.0
    if temp <= 66:
        red = 255
        green = 99.4708 * np.log(temp) - 161.119
    else:
        red = 329.6987 * ((temp - 60) -0.1332)
        green = 288.1222 * ((temp - 60) ** -0.0755)
    blue = 126.4 if temp <= 19 else 255
    
    # 归一化增益系数
    return np.clip([red/255, green/255, blue/255], 0.01, 2.0)

def apply_color_temp(np_img, kelvin):
    """应用色温调整的矩阵运算"""
    gains = kelvin_to_rgb(kelvin)
    adjusted = np_img * gains  # 广播机制应用通道增益
    return np.clip(adjusted * 255, 0, 255).astype(np.uint8)


def auto_levels(image, low_cut=0.1, high_cut=0.1):
    """
    自动色阶功能实现
    :param image: PIL Image对象
    :param low_cut: 低光裁剪比例（百分比）
    :param high_cut: 高光裁剪比例（百分比）
    :return: 处理后的PIL Image对象
    """
    # 将图像转换为RGB模式并转为NumPy数组
    img_array = np.array(image.convert('RGB'))

    # 分离RGB通道
    r = img_array[:,:,0].astype(np.float32)
    g = img_array[:,:,1].astype(np.float32)
    b = img_array[:,:,2].astype(np.float32)

    # 处理每个通道
    for channel in [r, g, b]:
        # 计算直方图[3,7](@ref)
        hist, bins = np.histogram(channel.flatten(), 256, [0,256])
        total_pixels = channel.size

        # 计算低光阈值
        cumulative = 0
        for i in range(256):
            cumulative += hist[i]
            if cumulative > total_pixels * low_cut / 100:
                min_level = i
                break

        # 计算高光阈值
        cumulative = 0
        for i in reversed(range(256)):
            cumulative += hist[i]
            if cumulative > total_pixels * high_cut / 100:
                max_level = i
                break

        # 线性映射[10,11](@ref)
        if max_level > min_level:
            channel[:] = np.clip((channel - min_level) * 255.0 / (max_level - min_level), 0, 255)

    # 合并通道并转换回图像
    return Image.fromarray(np.stack([r, g, b], axis=2).astype(np.uint8))

def rgb_to_hsv(img_array):
    """将RGB数组转换为HSV数组（手动实现）"""
    r, g, b = img_array[:,:,0]/255.0, img_array[:,:,1]/255.0, img_array[:,:,2]/255.0
    maxc = np.max(img_array/255.0, axis=2)
    minc = np.min(img_array/255.0, axis=2)
    diff = maxc - minc

    # 计算色相H
    h = np.zeros_like(maxc)
    mask = (maxc == r) & (diff != 0)
    h[mask] = (60 * ((g[mask]-b[mask])/diff[mask]) + 360) % 360
    mask = (maxc == g) & (diff != 0)
    h[mask] = (60 * ((b[mask]-r[mask])/diff[mask]) + 120) % 360
    mask = (maxc == b) & (diff != 0)
    h[mask] = (60 * ((r[mask]-g[mask])/diff[mask]) + 240) % 360

    # 转换到0-255范围
    h = (h / 360 * 255).astype(np.uint8)
    s = np.where(maxc != 0, (diff / maxc) * 255, 0).astype(np.uint8)
    v = (maxc * 255).astype(np.uint8)

    return np.stack([h, s, v], axis=2)

def hsv_to_rgb(hsv_array):
    """将HSV数组转换回RGB数组"""
    h, s, v = hsv_array[:,:,0]/255.0 * 360, hsv_array[:,:,1]/255.0, hsv_array[:,:,2]/255.0
    c = v * s
    x = c * (1 - np.abs((h/60) % 2 - 1))
    m = v - c

    rgb = np.zeros_like(hsv_array, dtype=np.float32)
    mask = (h >= 0) & (h < 60)
    rgb[mask] = np.stack([c[mask], x[mask], np.zeros_like(c[mask])], axis=-1)
    mask = (h >= 60) & (h < 120)
    rgb[mask] = np.stack([x[mask], c[mask], np.zeros_like(c[mask])], axis=-1)
    mask = (h >= 120) & (h < 180)
    rgb[mask] = np.stack([np.zeros_like(c[mask]), c[mask], x[mask]], axis=-1)
    mask = (h >= 180) & (h < 240)
    rgb[mask] = np.stack([np.zeros_like(c[mask]), x[mask], c[mask]], axis=-1)
    mask = (h >= 240) & (h < 300)
    rgb[mask] = np.stack([x[mask], np.zeros_like(c[mask]), c[mask]], axis=-1)
    mask = (h >= 300) & (h < 360)
    rgb[mask] = np.stack([c[mask], np.zeros_like(c[mask]), x[mask]], axis=-1)

    return ((rgb + m[...,np.newaxis]) * 255).clip(0,255).astype(np.uint8)

def hist_equalize_for_channel(channel):
    """直方图均衡化核心算法"""
    hist = np.histogram(channel, bins=256, range=(0,255))[0]
    cdf = hist.cumsum()
    cdf = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    return np.round(cdf[channel]).astype(np.uint8)

def hist_equalize(img):
    """主处理函数
    可用，但是图片出现断层了
    """
    # 读取图像并转换为HSV空间
    hsv = rgb_to_hsv(np.array(img))

    # 对V通道进行均衡化
    v_eq = hist_equalize_for_channel(hsv[:,:,2])
    hsv_eq = np.stack([hsv[:,:,0], hsv[:,:,1], v_eq], axis=2)

    # 转换回RGB并保存
    return Image.fromarray(hsv_to_rgb(hsv_eq))