import argparse
import os
from PIL import Image


def convert_png_to_jpg(root_dir, output_dir, quality=95, lowest=0.5, verbose=False):
    """
    Convert PNG files to JPG format while maintaining directory structure.
    
    Args:
        root_dir (str): The root directory containing PNG files to convert
        output_dir (str): The output directory for JPG files
        quality (int): JPG quality (0-100, default: 95)
        lowest (float): Minimum file size in MB to apply quality reduction (default: 0.5)
        verbose (bool): Enable verbose output (default: False)
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png'):
                os.makedirs(output_dir, exist_ok=True)
                # Create relative path from root_dir to get target subdirectory
                rel_path = os.path.relpath(root, root_dir)
                output_subdir = os.path.join(output_dir, rel_path)
                os.makedirs(output_subdir, exist_ok=True)
        
                png_path = os.path.join(root, file)
                # Create jpg path in target directory structure
                jpg_name = os.path.splitext(file)[0] + '.jpg'
                jpg_path = os.path.join(output_subdir, jpg_name)
                
                if os.path.getsize(png_path) < lowest * 1024 * 1024:
                    if verbose:
                        print(f"Keep the original quality because it's too small")
                    _quality = 100
                else:
                    _quality = quality
            
                try:
                    with Image.open(png_path) as img:
                        rgb_img = img.convert('RGB')
                        rgb_img.save(jpg_path, 'JPEG', quality=_quality)
                    if verbose:
                        print(f"Converted: {png_path} -> {jpg_path}")
                except Exception as e:
                    if verbose:
                        print(f"Failed to convert {png_path}: {e}")


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description='Convert PNG files to JPG in a directory.')
    parser.add_argument('-d', '--directory', type=str, required=True, 
                       help='The root directory for PNG conversion')
    parser.add_argument('-o', '--output', default='lower', type=str, 
                       help='The output directory for JPG output')
    parser.add_argument('-q', '--quality', type=int, default=50, 
                       help='The quality of the JPG image')
    parser.add_argument('-l', '--lowest', type=float, default=0.5, 
                       help='The lowest file size to convert in MB')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Verbose output')
    args = parser.parse_args()

    if os.path.isdir(args.directory):
        convert_png_to_jpg(args.directory, args.output, args.quality, args.lowest, args.verbose)
    else:
        print("Invalid directory. Please try again.")


if __name__ == '__main__':
    main() 