from compress import compress_images  # Make sure compress_images can handle both modes
import os

def get_input(prompt, default, validation=lambda x: True, error_msg=""):
    """Simplified input handler with defaults and validation"""
    while True:
        try:
            value = input(prompt) or default
            if validation(value):
                return value
            print(error_msg)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            exit()
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("## Image Compression Tool ##")

    # Get user inputs with defaults and validation
    input_folder = get_input(
        "Input folder [input_images]: ",
        "input_images",
        lambda x: os.path.isdir(x),
        "Folder doesn't exist"
    )

    output_folder = get_input(
        "Output folder [output_images]: ",
        "output_images"
    )

    quality = int(get_input(
        "Quality (1-90) [75]: ",
        "75",
        lambda x: x.isdigit() and 1 <= int(x) <= 90,
        "Must be 1-90"
    ))

    method = get_input(
        "Choose compression method:\n(1) Simple JPEG\n(2) DCT-based analysis\n: ",
        "1",
        lambda x: x in ["1", "2"],
        "Please enter 1 or 2"
    )

    try:
        if method == "1":
            print(f"\nCompressing using standard JPEG method at quality {quality}...")
            compress_images(input_folder, output_folder, quality=quality)
        else:
            print(f"\nRunning DCT-based luminance compression at quality {quality}...")
            compress_images(input_folder, output_folder, quality=quality, use_dct=True)

        print(f"\nOutput saved to: {os.path.abspath(output_folder)}")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    while True:
        main()
