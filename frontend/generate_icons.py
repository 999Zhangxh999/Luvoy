#!/usr/bin/env python3
"""Generate Android app icons from a source image."""

from PIL import Image
import os

# Source logo
SOURCE = r"e:\work\Luvoy\Luvoy\frontend\logo.png"

# Android icon sizes (dp -> px)
MIPMAP_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# Android foreground icon sizes (for adaptive icons, larger)
FOREGROUND_SIZES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

RES_DIR = r"e:\work\Luvoy\Luvoy\frontend\android\app\src\main\res"

def create_icon(img, size, output_path):
    """Resize image to specified size and save."""
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(output_path, "PNG")
    print(f"Created: {output_path} ({size}x{size})")

def create_round_icon(img, size, output_path):
    """Create a round icon with transparent background."""
    # Create a new image with transparency
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create circular mask
    from PIL import ImageDraw
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(resized, (0, 0))
    output.putalpha(mask)
    output.save(output_path, "PNG")
    print(f"Created: {output_path} (round, {size}x{size})")

def create_foreground_icon(img, size, output_path):
    """Create foreground icon with padding for adaptive icons."""
    # For adaptive icons, the safe zone is 66/108 of the total size
    # So we need to add padding around the icon
    padding = int(size * 0.2)  # 20% padding on each side
    icon_size = size - (padding * 2)
    
    # Resize the icon
    resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    
    # Create output with transparent background
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(resized, (padding, padding))
    output.save(output_path, "PNG")
    print(f"Created: {output_path} (foreground, {size}x{size})")

def main():
    # Open source image
    img = Image.open(SOURCE)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    print(f"Source image: {SOURCE}")
    print(f"Original size: {img.size}")
    print()
    
    # Generate icons for each density
    for folder, size in MIPMAP_SIZES.items():
        folder_path = os.path.join(RES_DIR, folder)
        
        # ic_launcher.png
        create_icon(img, size, os.path.join(folder_path, "ic_launcher.png"))
        
        # ic_launcher_round.png
        create_round_icon(img, size, os.path.join(folder_path, "ic_launcher_round.png"))
    
    # Generate foreground icons for adaptive icons
    for folder, size in FOREGROUND_SIZES.items():
        folder_path = os.path.join(RES_DIR, folder)
        create_foreground_icon(img, size, os.path.join(folder_path, "ic_launcher_foreground.png"))
    
    print()
    print("All icons generated successfully!")

if __name__ == "__main__":
    main()
