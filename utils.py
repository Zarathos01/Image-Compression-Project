import numpy as np
from PIL import Image
import cv2

def jpeg_luminance_compression(image: Image.Image, quality=75) -> list:
    """
    Advanced compression with quantization table scaling.
    Returns DCT coefficients for analysis and the reconstructed image.

    Args:
        image: PIL Image object
        quality: 1-100 (higher = less compression)
    Returns:
        List of compressed DCT coefficient blocks, Reconstructed Image
    """
    # Quality to scale factor conversion (standard JPEG scaling)
    quality = max(1, min(90, quality))
    scale = 5000 / quality if quality < 50 else 200 - 2 * quality

    # Standard luminance quantization table
    quant_table = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float32)

    # Scale quantization table
    scaled_table = np.clip(np.floor((quant_table * scale + 50) / 100), 1, 255)

    # Convert to YCbCr and get Y channel
    ycbcr = image.convert("YCbCr")
    y, _, _ = ycbcr.split()
    y_arr = np.array(y, dtype=np.float32)

    # Pad image to multiple of 8
    h, w = y_arr.shape
    padded = np.pad(y_arr, ((0, (8 - h % 8) % 8), (0, (8 - w % 8) % 8)),
                    mode='constant', constant_values=0)
    shifted = padded - 128  # Level shift

    # Zigzag pattern
    zigzag_indices = [
        (0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
        (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 5),
        (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
        (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
        (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
        (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
        (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
        (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)
    ]

    # Process blocks
    compressed = []
    for i in range(0, padded.shape[0], 8):
        for j in range(0, padded.shape[1], 8):
            block = shifted[i:i + 8, j:j + 8]
            dct_block = cv2.dct(block)
            quantized = np.round(dct_block / scaled_table)

            # Zigzag scan and truncate zeros
            zigzag = [int(quantized[x, y]) for x, y in zigzag_indices]
            while len(zigzag) > 1 and zigzag[-1] == 0:
                zigzag.pop()
            compressed.append(zigzag)

    # Reconstruct image from quantized DCT
    reconstructed = np.zeros_like(padded)
    block_idx = 0
    for i in range(0, padded.shape[0], 8):
        for j in range(0, padded.shape[1], 8):
            # Dequantize
            block = np.zeros((8, 8), dtype=np.float32)
            zigzag = compressed[block_idx]
            for idx, (x, y) in enumerate(zigzag_indices):
                if idx < len(zigzag):
                    block[x, y] = zigzag[idx]
            idct_block = cv2.idct(block * scaled_table)
            reconstructed[i:i + 8, j:j + 8] = idct_block
            block_idx += 1

    # Reverse level shift and clip to valid range
    reconstructed += 128
    reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)

    # Convert to Image object
    result_img = Image.fromarray(reconstructed[:h, :w], mode='L')
    return compressed, result_img
