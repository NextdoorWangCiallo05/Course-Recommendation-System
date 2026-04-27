from PIL import Image
import os

images_dir = r'd:\Select\frontend\public\images'

for filename in os.listdir(images_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    filepath = os.path.join(images_dir, filename)
    original_size = os.path.getsize(filepath)
    
    img = Image.open(filepath)
    
    # 限制最大宽度为 1920px（适配 1080p 屏幕）
    max_width = 1920
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    # 转 RGB 并保存为高质量 JPEG
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGBA')
        # 如果有透明背景，合成到白色背景上
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 保存为 JPEG，质量 85
    new_filename = filename.rsplit('.', 1)[0] + '.jpg'
    output_path = os.path.join(images_dir, new_filename)
    img.save(output_path, 'JPEG', quality=85, optimize=True)
    
    new_size = os.path.getsize(output_path)
    ratio = (1 - new_size / original_size) * 100
    print(f'{filename} ({original_size//1024}KB) -> {new_filename} ({new_size//1024}KB, {img.size[0]}x{img.size[1]}) 减小 {ratio:.0f}%')

print('压缩完成')
