from PIL import Image
from tqdm import tqdm
import numpy as np
import svgwrite
import os
import re

# Set input image path
set_input_file = "input/typezero.png"
# Set image width (default is 600)
set_width = 2048
# Set output directory
set_output_directory = "output"
# Enable SVG export?
set_svg_export = False
# Image sequence?
is_sequence = False

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
    # Check if the output directory exists, create if not
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image.save(output_path, 'PNG')

# Updated dithering engine
def dithering_engine(image_path, base_width=600):
    image = read_and_convert_image(image_path)
    scaled_image = scale_image(image, base_width)
    dithered_image = atkinson_dithering(scaled_image)

    # Generate output filenames with suffix
    base_filename, file_extension = os.path.splitext(os.path.basename(image_path))
    output_suffix = f'_dither_{base_width}'
    output_png_path = os.path.join(set_output_directory, f'{base_filename}{output_suffix}.png')
    
    # Save as PNG
    save_to_png(dithered_image, output_png_path)

    # Check if SVG export is enabled
    if set_svg_export:
        output_svg_path = os.path.join(set_output_directory, f'{base_filename}{output_suffix}.svg')
        optimized_svg(dithered_image, output_svg_path)

# Image sequence handling
# Find image sequence based on the input filename
def find_image_sequence(directory, base_filename, extension, frame_length):
    pattern = re.compile(rf"{re.escape(base_filename)}\d{{{frame_length}}}\{extension}$")
    return [f for f in os.listdir(directory) if pattern.match(f)]

# Updated dithering engine to handle sequences
def dithering_engine(image_path, base_width=600, is_sequence=False):
    directory, filename = os.path.split(image_path)
    base_filename, extension = os.path.splitext(filename)
    
    # Process image sequences if is_sequence is True
    if is_sequence:
        frame_length = len(re.search(r'\d+$', base_filename).group())
        images = find_image_sequence(directory, base_filename[:-frame_length], extension, frame_length)
        for img in images:
            process_image(os.path.join(directory, img), base_width)
    else:
        process_image(image_path, base_width)

# Function to process each image
def process_image(image_path, base_width):
    image = read_and_convert_image(image_path)
    scaled_image = scale_image(image, base_width)
    dithered_image = atkinson_dithering(scaled_image)

    # Generate output filenames with suffix
    base_filename, file_extension = os.path.splitext(os.path.basename(image_path))
    output_suffix = f'_dither_{base_width}'
    output_png_path = os.path.join(set_output_directory, f'{base_filename}{output_suffix}.png')
    
    # Save as PNG
    save_to_png(dithered_image, output_png_path)

    # Check if SVG export is enabled
    if set_svg_export:
        output_svg_path = os.path.join(set_output_directory, f'{base_filename}{output_suffix}.svg')
        optimized_svg(dithered_image, output_svg_path)

# Execute the dithering engine
dithering_engine(set_input_file, set_width, is_sequence)