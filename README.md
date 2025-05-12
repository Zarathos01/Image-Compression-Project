-> Image Compression Tool

A Python-based image compression tool that offers both standard JPEG and advanced DCT-based luminance compression methods.

> Features

- Two Compression Methods:
  - Standard JPEG compression
  - Advanced DCT-based luminance compression with customizable quality settings
- Quality Control: Adjustable compression quality (1-90)
- Format Support: Works with JPG, JPEG, PNG, BMP, and WEBP formats
- Detailed Output: Shows compression ratios and file size savings

> Usage

1. Place your images in an `input_images` folder (or specify your own input folder)
2. Run the program:
   ```bash
   python main.py
   ```
3. Follow the interactive prompts to:
   - Select input/output folders
   - Choose compression quality (1-90)
   - Select compression method (standard JPEG or DCT-based)
4. Compressed images will be saved in the output folder with quality and method tags

> Technical Details

The DCT-based compression method:
- Uses luminance channel (Y) from YCbCr color space
- Applies Discrete Cosine Transform (DCT) on 8x8 blocks
- Implements quantization with standard JPEG luminance table
- Includes zigzag scanning and zero truncation
- Reconstructs image from quantized coefficients


> Requirements

- Python 3.6+
- Pillow (PIL fork)
- OpenCV (cv2)
- NumPy

> License

This project is open source and available under the MIT License.
