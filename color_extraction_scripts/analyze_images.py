#!/usr/bin/env python3
"""
Wheel Color Extraction Tool
Analyzes autism trait wheel images to extract hex color values
"""

import json
import math
from PIL import Image
import os

# Image paths
IMAGE_DIR = "references/wheel"
IMAGE_FILES = [
    "Wheel of Autism.png",
    "Wheel of Autism 2.png",
    "Wheel of Autism 3.png"
]

def analyze_image_dimensions():
    """Analyze dimensions of all wheel images"""
    for filename in IMAGE_FILES:
        filepath = os.path.join(IMAGE_DIR, filename)
        if os.path.exists(filepath):
            with Image.open(filepath) as img:
                print(f"\n{filename}:")
                print(f"  Dimensions: {img.width} x {img.height}")
                print(f"  Mode: {img.mode}")

                # For the main wheel images (2 & 3), estimate center point
                if "2.png" in filename or "3.png" in filename:
                    # These should be single wheel images
                    center_x = img.width // 2
                    center_y = img.height // 2
                    print(f"  Estimated center: ({center_x}, {center_y})")
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    print("=== Wheel Image Analysis ===")
    analyze_image_dimensions()