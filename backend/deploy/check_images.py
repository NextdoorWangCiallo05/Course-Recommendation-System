from PIL import Image
import os

images_dir = r'd:\Select\frontend\public\images'

for filename in os.listdir(images_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    filepath = os.path.join(images_dir, filename)
    img = Image.open(filepath)
    print(f'{filename}: {img.size[0]}x{img.size[1]}, {os.path.getsize(filepath)//1024}KB')
