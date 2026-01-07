#!/usr/bin/env python3
"""
Advanced Wheel Analysis Tool
Finds precise center and radius of the color wheels
"""

import json
import math
from PIL import Image, ImageDraw
import os
import numpy as np

# The 12 traits in clockwise order starting from top (0°)
TRAITS = [
    "Emotional Regulation",
    "Social Interaction",
    "Speech",
    "Sensory Sensitivities",
    "Nonverbal Communication",
    "Perception",
    "Executive Functions",
    "Intense Interests",
    "Cognitive Flexibility",
    "Repetitive Behaviors",
    "Motor Skills/Coordination",
    "Sensory Processing"
]

def find_wheel_center_and_radius(image_path, debug=False):
    """
    Find the center and radius of the wheel by analyzing the image
    """
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        width, height = img.size

        # Start with estimated center
        est_center_x = width // 2
        est_center_y = height // 2

        print(f"\nAnalyzing {os.path.basename(image_path)}:")
        print(f"  Image size: {width}x{height}")
        print(f"  Estimated center: ({est_center_x}, {est_center_y})")

        # Sample some points to find the wheel boundaries
        # Check for dark center circle
        center_color = img.getpixel((est_center_x, est_center_y))
        print(f"  Center color: {center_color}")

        # Find inner radius by moving outward from center until color changes significantly
        inner_radius = find_inner_radius(img, est_center_x, est_center_y)
        print(f"  Inner radius (dark center): ~{inner_radius}px")

        # Find outer radius by looking for the edge of colored segments
        outer_radius = find_outer_radius(img, est_center_x, est_center_y, inner_radius)
        print(f"  Outer radius: ~{outer_radius}px")

        # Calculate the 5 intensity level radii
        ring_width = (outer_radius - inner_radius) / 5
        level_radii = []
        for i in range(1, 6):
            radius = inner_radius + (ring_width * i) - (ring_width / 2)
            level_radii.append(int(radius))

        print(f"  Level radii: {level_radii}")

        return {
            'center_x': est_center_x,
            'center_y': est_center_y,
            'inner_radius': inner_radius,
            'outer_radius': outer_radius,
            'level_radii': level_radii
        }

def find_inner_radius(img, center_x, center_y):
    """Find the radius of the inner dark circle"""
    # Start from center and move outward until we hit non-dark color
    for radius in range(1, 200):
        # Check color at this radius in multiple directions
        for angle in [0, 90, 180, 270]:  # 4 directions
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))

            if 0 <= x < img.width and 0 <= y < img.height:
                r, g, b = img.getpixel((x, y))
                # If we find a color that's not very dark, we've found the edge
                if r > 50 or g > 50 or b > 50:  # Not dark
                    return radius
    return 50  # Default fallback

def find_outer_radius(img, center_x, center_y, inner_radius):
    """Find the outer radius of the wheel"""
    # Start from inner radius and move outward until we hit background
    max_radius = min(center_x, center_y, img.width - center_x, img.height - center_y)

    for radius in range(inner_radius + 100, max_radius):
        # Check multiple angles to see if we're still in wheel area
        colored_count = 0
        total_checks = 12

        for i in range(total_checks):
            angle = (360 / total_checks) * i
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))

            if 0 <= x < img.width and 0 <= y < img.height:
                r, g, b = img.getpixel((x, y))
                # Check if this looks like wheel content vs background
                # Background is typically white/light, wheel has colors or gray
                if r < 240 or g < 240 or b < 240:  # Not white background
                    colored_count += 1

        # If less than half the points are colored, we've probably hit the edge
        if colored_count < total_checks * 0.5:
            return radius - 20  # Back off a bit from the edge

    return max_radius - 50  # Default fallback

def sample_color_at_position(img, center_x, center_y, angle_deg, radius):
    """Sample color at a specific angle and radius from center"""
    # Convert angle to radians and adjust for our coordinate system
    # 0° should be at top, increasing clockwise
    angle_rad = math.radians(angle_deg - 90)  # Adjust so 0° is at top

    x = int(center_x + radius * math.cos(angle_rad))
    y = int(center_y + radius * math.sin(angle_rad))

    # Make sure coordinates are within image bounds
    if 0 <= x < img.width and 0 <= y < img.height:
        return img.getpixel((x, y))
    return None

def rgb_to_hex(r, g, b):
    """Convert RGB values to hex string"""
    return f"#{r:02x}{g:02x}{b:02x}"

def analyze_wheel_image(image_path):
    """Complete analysis of a wheel image"""
    wheel_data = find_wheel_center_and_radius(image_path)

    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Sample colors for each trait and level
        colors = {}
        center_x = wheel_data['center_x']
        center_y = wheel_data['center_y']
        level_radii = wheel_data['level_radii']

        for i, trait in enumerate(TRAITS):
            angle = i * 30  # 30 degrees per trait
            trait_colors = {}

            for level in range(1, 6):
                radius = level_radii[level - 1]
                color = sample_color_at_position(img, center_x, center_y, angle, radius)

                if color:
                    r, g, b = color
                    hex_color = rgb_to_hex(r, g, b)
                    trait_colors[str(level)] = hex_color
                    print(f"  {trait} L{level} (r={radius}, a={angle}°): {hex_color}")
                else:
                    trait_colors[str(level)] = None
                    print(f"  {trait} L{level}: OUT_OF_BOUNDS")

            colors[trait] = trait_colors

    return colors

if __name__ == "__main__":
    print("=== Advanced Wheel Analysis ===")

    # Analyze the primary image (Wheel of Autism 3.png)
    primary_image = "references/wheel/Wheel of Autism 3.png"
    if os.path.exists(primary_image):
        colors = analyze_wheel_image(primary_image)

        # Save results
        with open("extracted_colors.json", "w") as f:
            json.dump(colors, f, indent=2)
        print(f"\nColors saved to extracted_colors.json")
    else:
        print(f"Primary image not found: {primary_image}")