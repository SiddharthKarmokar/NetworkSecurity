from PIL import Image
import os

image_folder = 'images'
output_gif = 'slider.gif'

images = [img for img in os.listdir(image_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
images.sort()

frames = [Image.open(os.path.join(image_folder, img)) for img in images]

frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=800, 
    loop=0  
)

print(f"GIF saved as {output_gif}")
