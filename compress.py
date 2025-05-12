import os
from PIL import Image
from utils import jpeg_luminance_compression

def compress_images(input_folder, output_folder, quality=75, use_dct=False):
    """
    Compresses images using either standard JPEG or DCT analysis mode.

    Args:
        input_folder: Path to input images
        output_folder: Path to save compressed images
        quality: JPEG quality (1-100 where 1=worst, 100=best)
        use_dct: If True, uses DCT-based algorithm; otherwise standard JPEG compression
    """
    os.makedirs(output_folder, exist_ok=True)
    supported = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    for fname in os.listdir(input_folder):
        if not fname.lower().endswith(supported):
            print(f"Skipping {fname} - unsupported format")
            continue
        trail = ''
        if use_dct:
            trail = 'dct'
        else:
            trail = 'std'
        in_path = os.path.join(input_folder, fname)
        base, _ = os.path.splitext(fname)
        out_path = os.path.join(output_folder, base + f"_{quality}_{trail}.jpg")

        with Image.open(in_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')

            original_size = os.path.getsize(in_path)

            if use_dct:
                # DCT-based compression
                compressed, reconstructed_img = jpeg_luminance_compression(img, quality=quality)

                # Convert grayscale (Y channel) back to RGB for saving
                final_img = Image.merge("YCbCr", (reconstructed_img, *img.convert("YCbCr").split()[1:])).convert("RGB")
                final_img.save(out_path, "JPEG", optimize=True)

                new_size = os.path.getsize(out_path)

                print(f"{fname}: {original_size / 1024:.1f}KB → {new_size / 1024:.1f}KB "
                      f"(Quality: {quality}, {new_size / original_size * 100:.1f}%) ")
                      
            else:
                # Standard JPEG compression
                img.save(out_path, "JPEG", quality=quality, optimize=True)
                new_size = os.path.getsize(out_path)

                print(f"{fname}: {original_size / 1024:.1f}KB → {new_size / 1024:.1f}KB "
                      f"(Quality: {quality}, {new_size / original_size * 100:.1f}%)")
