# Image Dithering Engine 🎨🖼️

This Python script applies the Atkinson dithering algorithm to images, converting them to a stylized 1-bit grayscale format. The output is available in PNG and optionally in SVG formats.

## Features 🌟

- **Atkinson Dithering**: Applies the Atkinson dithering algorithm for a classic dithered look.
- **Output Formats**: Generates PNG files, with an option to also generate SVG files.
- **Configurable Width**: Allows setting a custom width for the output image.
- **Output Directory**: Specify a directory for output files.
- **Optional SVG Output**: Control whether to generate SVG files alongside PNG files.

## Requirements 📋

To run this script, you need Python installed on your system along with the following libraries:
- PIL (Pillow)
- Numpy
- svgwrite (only if SVG output is enabled)
- tqdm

You can install these dependencies using:

```pip install pillow numpy svgwrite tqdm```

## Usage 🚀

1. **Set Parameters**: 
   - Edit the `set_input_file`, `set_width`, `set_output_directory`, and `set_svg_export` variables at the top of the script as per your requirements.

2. **Run the Script**:
   - Execute the Python script. Output files (PNG and optionally SVG) will be generated in the specified output directory.

## Output Files 📁

- **PNG File**: Stored in the specified output directory with the format `originalfilename_dither_width.png`.
- **SVG File** (if enabled): Stored in the same directory with the format `originalfilename_dither_width.svg`.

The suffix `_dither_width` in the filenames represents the width setting used during dithering.

## Example 📷

Given an input file `foobar.jpg`, a width setting of `512`, and output directory `output`, with SVG export enabled, the output files will be named `output/foobar_dither_512.png` and `output/foobar_dither_512.svg`.

## Notes 📝

- The script is optimized for 1-bit grayscale images. For best results, use images with a clear contrast.
- SVG output is optimized for smaller sizes and may not be suitable for very large images.
- Ensure the output directory exists or modify the script to create it if necessary.

## Contributing 🤝

Feel free to fork this repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License 📄

This project is open source and available under the [ISC License](LICENSE).

---

Happy Dithering! 🌈👨‍🎨
🖤 *izzy*