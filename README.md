# Image Dithering Engine 🎨🖼️

This Python script applies the Atkinson dithering algorithm to images, converting them into a stylized 1-bit grayscale format. The output is available in both PNG and SVG formats.

## Features 🌟

- **Atkinson Dithering**: Applies the Atkinson dithering algorithm for a classic dithered look.
- **Output Formats**: Generates both SVG and PNG files.
- **Configurable Width**: Allows setting a custom width for the output image.
- **Automatic Filename Handling**: Output files are automatically named based on the input filename and settings.

## Requirements 📋

To run this script, you need Python installed on your system along with the following libraries:
- PIL (Pillow)
- Numpy
- svgwrite
- tqdm

You can install these dependencies using:

```
pip install pillow numpy svgwrite tqdm
```

## Usage 🚀

1. **Set Input File and Width**: 
   - Edit the `set_input_file` and `set_width` variables at the top of the script to your desired input file and image width.

2. **Run the Script**:
   - Simply execute the Python script. Output files (PNG and SVG) will be generated in the same directory as the input file.

## Output Files 📁

- **PNG File**: `originalfilename_dither_width.png`
- **SVG File**: `originalfilename_dither_width.svg`

The suffix `_dither_width` in the filenames represents the width setting used during dithering.

## Example 📷

Given an input file `image.png` and a width setting of `255`, the output files will be named `image_dither_255.png` and `image_dither_255.svg`.

## Notes 📝

- The script is optimized for 1-bit grayscale images. For best results, use images with a clear contrast.
- SVG output is optimized for smaller sizes and may not be suitable for very large images.

## Contributing 🤝

Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License 📄

This project is open source and available under the [MIT License](LICENSE).

---

Happy Dithering! 🌈👨‍🎨