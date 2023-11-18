from PIL import Image
from tqdm import tqdm
import numpy as np
import svgwrite
import os

# Set input image path
set_input_file = "image.png"
# Set image width (default is 600)
set_width = 255

# Read and convert image to grayscale
def read_and_convert_image(image_path):
    image = Image.open(image_path)
    return image.convert('L')

# Scale image while keeping aspect ratio
def scale_image(image, base_width=600):
    w_percent = (base_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    return image.resize((base_width, h_size), Image.Resampling.NEAREST)

# Atkinson Dithering algorithm implementation
def atkinson_dithering(image):
    img_array = np.array(image)
    height, width = img_array.shape
    for y in tqdm(range(height), desc='Dithering'):
        for x in range(width):
            old_pixel = img_array[y, x]
            new_pixel = 255 * (old_pixel // 128)
            img_array[y, x] = new_pixel
            error = old_pixel - new_pixel
            if x + 1 < width:
                img_array[y, x+1] += error * 1/8
            if x + 2 < width:
                img_array[y, x+2] += error * 1/8
            if x > 0 and y + 1 < height:
                img_array[y+1, x-1] += error * 1/8
            if y + 1 < height:
                img_array[y+1, x] += error * 1/8
            if y + 2 < height:
                img_array[y+2, x] += error * 1/8
            if x + 1 < width and y + 1 < height:
                img_array[y+1, x+1] += error * 1/8
    return Image.fromarray(np.uint8(img_array), 'L')

# Optimized SVG generation
def optimized_svg(image, output_path):
    img_array = np.array(image)
    height, width = img_array.shape
    dwg = svgwrite.Drawing(output_path, (width, height))
    for y in tqdm(range(height), desc='SVG Generation'):
        x_start = 0
        current_color = int(img_array[y, 0])
        for x in range(1, width):
            new_color = int(img_array[y, x])
            if new_color != current_color:
                dwg.add(dwg.rect((x_start, y), (x - x_start, 1), fill=svgwrite.rgb(current_color, current_color, current_color)))
                x_start = x
                current_color = new_color
        dwg.add(dwg.rect((x_start, y), (width - x_start, 1), fill=svgwrite.rgb(current_color, current_color, current_color)))
    dwg.save()

# Save the dithered image as a PNG
def save_to_png(image, output_path):
    image.save(output_path, 'PNG')

# Updated dithering engine
def dithering_engine(image_path, output_svg_path, output_png_path=None, base_width=600):
    image = read_and_convert_image(image_path)
    scaled_image = scale_image(image, base_width)
    dithered_image = atkinson_dithering(scaled_image)
    optimized_svg(dithered_image, output_svg_path)
    if output_png_path:
        save_to_png(dithered_image, output_png_path)

# Generate output filenames with suffix
input_image_path = set_input_file
base_filename, file_extension = os.path.splitext(input_image_path)
output_suffix = f'_dither_{set_width}'
output_png_path = f'{base_filename}{output_suffix}.png'
output_svg_path = f'{base_filename}{output_suffix}.svg'

# Execute the dithering engine
dithering_engine(input_image_path, output_svg_path, output_png_path, set_width)