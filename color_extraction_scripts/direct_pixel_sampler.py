#!/usr/bin/env python3
"""
Direct Pixel Sampler for Autism Wheel Colors
Directly samples pixel colors from the wheel images at precise coordinates
NO INTERPOLATION - ONLY ACTUAL PIXEL SAMPLING
"""

import json
import math
from PIL import Image, ImageDraw
import os

# The 12 traits in clockwise order with their segment midpoint angles (corrected positioning)
TRAITS_WITH_ANGLES = {
    "Emotional Regulation": 15,          # Top-right (corrected from Sensory Processing)
    "Social Interaction": 45,            # Upper right (corrected from Emotional Regulation)
    "Speech": 75,                        # Right (corrected from Social Interaction)
    "Sensory Sensitivities": 105,        # Lower right (corrected from Speech)
    "Nonverbal Communication": 135,      # Bottom right (corrected from Sensory Sensitivities)
    "Perception": 165,                   # Bottom center-right (corrected from Nonverbal Communication)
    "Executive Functions": 195,          # Bottom center-left (corrected from Perception)
    "Intense Interests": 225,            # Lower left (corrected from Executive Functions)
    "Cognitive Flexibility": 255,        # Left (corrected from Intense Interests)
    "Repetitive Behaviors": 285,         # Upper left (corrected from Cognitive Flexibility)
    "Motor Skills/Coordination": 315,    # Top left (corrected from Repetitive Behaviors)
    "Sensory Processing": 345            # Top center-left (corrected from Motor Skills/Coordination)
}

# Intensity level radii from center (corrected to align with actual ring centers)
LEVEL_RADII = {
    1: 118,  # Innermost ring (lightest) - Ring 1 center
    2: 228,  # Ring 2 center
    3: 308,  # Ring 3 center
    4: 389,  # Ring 4 center
    5: 470   # Outermost ring (most intense) - Ring 5 center
}

# Image configurations
IMAGE_CONFIGS = {
    "image2": {
        "path": "../references/wheel/Wheel of Autism 2.png",
        "center_x": 1243,
        "center_y": 698
    },
    "image3": {
        "path": "../references/wheel/Wheel of Autism 3.png",
        "center_x": 1242,
        "center_y": 697
    }
}

def rgb_to_hex(r, g, b):
    """Convert RGB values to hex string"""
    return f"#{r:02x}{g:02x}{b:02x}"

def is_gray_color(r, g, b, threshold=25):
    """
    Determine if a color is gray (inactive) based on RGB similarity
    Gray colors have very similar R, G, B values
    """
    max_diff = max(abs(r-g), abs(g-b), abs(r-b))
    return max_diff < threshold

def sample_pixel_at_coordinates(image, x, y):
    """
    Sample pixel color at specific coordinates
    Returns (r, g, b) tuple or None if out of bounds
    """
    if 0 <= x < image.width and 0 <= y < image.height:
        return image.getpixel((int(x), int(y)))
    return None

def calculate_sampling_coordinates(center_x, center_y, angle_degrees, radius):
    """
    Calculate pixel coordinates for sampling
    angle_degrees: angle in degrees (0° = top, clockwise)
    """
    # Convert to radians and adjust so 0° is at top of wheel
    angle_rad = math.radians(angle_degrees - 90)

    x = center_x + radius * math.cos(angle_rad)
    y = center_y + radius * math.sin(angle_rad)

    return int(x), int(y)

def sample_colors_from_images():
    """
    Sample colors from both wheel images using direct pixel sampling
    """
    print("=== Direct Pixel Sampling from Autism Wheel Images ===")

    # Load both images
    images = {}
    for img_key, config in IMAGE_CONFIGS.items():
        img_path = config["path"]
        if os.path.exists(img_path):
            img = Image.open(img_path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            images[img_key] = {
                'image': img,
                'center_x': config["center_x"],
                'center_y': config["center_y"]
            }
            print(f"✓ Loaded {img_path}")
        else:
            print(f"✗ Image not found: {img_path}")
            return None

    if len(images) != 2:
        print("ERROR: Both images are required for sampling")
        return None

    # Sample colors for all 60 segments
    sampled_colors = {}
    sampling_debug = []

    for trait, angle in TRAITS_WITH_ANGLES.items():
        print(f"\nSampling {trait} (angle {angle}°):")
        trait_colors = {}

        for level in range(1, 6):
            radius = LEVEL_RADII[level]

            # Sample from both images
            colors_found = {}

            for img_key, img_data in images.items():
                center_x = img_data['center_x']
                center_y = img_data['center_y']
                image = img_data['image']

                # Calculate sampling coordinates
                x, y = calculate_sampling_coordinates(center_x, center_y, angle, radius)

                # Sample the pixel
                pixel_color = sample_pixel_at_coordinates(image, x, y)

                if pixel_color:
                    r, g, b = pixel_color
                    hex_color = rgb_to_hex(r, g, b)
                    is_gray = is_gray_color(r, g, b)

                    colors_found[img_key] = {
                        'hex': hex_color,
                        'rgb': (r, g, b),
                        'coordinates': (x, y),
                        'is_gray': is_gray
                    }

                    gray_marker = " (GRAY)" if is_gray else " (COLORED)"
                    print(f"  {img_key} L{level} at ({x}, {y}): {hex_color}{gray_marker}")
                else:
                    print(f"  {img_key} L{level}: OUT_OF_BOUNDS")

            # Apply OR logic to choose the best color
            chosen_color = None
            chosen_source = None

            # Priority: 1) Non-gray from image3, 2) Non-gray from image2, 3) Gray from either
            if 'image3' in colors_found and not colors_found['image3']['is_gray']:
                chosen_color = colors_found['image3']
                chosen_source = 'image3'
            elif 'image2' in colors_found and not colors_found['image2']['is_gray']:
                chosen_color = colors_found['image2']
                chosen_source = 'image2'
            elif 'image3' in colors_found:
                chosen_color = colors_found['image3']
                chosen_source = 'image3 (gray)'
            elif 'image2' in colors_found:
                chosen_color = colors_found['image2']
                chosen_source = 'image2 (gray)'

            # Store result
            if chosen_color and not chosen_color['is_gray']:
                trait_colors[str(level)] = chosen_color['hex']
                print(f"  → SELECTED: {chosen_color['hex']} from {chosen_source}")
            else:
                trait_colors[str(level)] = None  # No non-gray color found
                gray_hex = chosen_color['hex'] if chosen_color else "#808080"
                print(f"  → NO COLOR FOUND: Only gray available ({gray_hex})")

            # Save debug info
            sampling_debug.append({
                'trait': trait,
                'level': level,
                'angle': angle,
                'radius': radius,
                'colors_found': colors_found,
                'chosen': chosen_color['hex'] if chosen_color else None,
                'source': chosen_source
            })

        sampled_colors[trait] = trait_colors

    return sampled_colors, sampling_debug

def create_debug_visualization(sampling_debug):
    """
    Create debug image showing sampling points on the wheel
    """
    print("\nCreating debug visualization...")

    # Use image 3 as base
    base_image_path = IMAGE_CONFIGS['image3']['path']
    if not os.path.exists(base_image_path):
        print("Cannot create debug visualization - base image not found")
        return

    with Image.open(base_image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        debug_img = img.copy()
        draw = ImageDraw.Draw(debug_img)

        center_x = IMAGE_CONFIGS['image3']['center_x']
        center_y = IMAGE_CONFIGS['image3']['center_y']

        # Draw center point
        draw.ellipse([center_x-5, center_y-5, center_x+5, center_y+5], fill='red', outline='white')

        # Draw sampling points
        for debug_info in sampling_debug:
            angle = debug_info['angle']
            radius = debug_info['radius']
            x, y = calculate_sampling_coordinates(center_x, center_y, angle, radius)

            # Color code the sampling points
            if debug_info['chosen']:
                color = 'lime'  # Green for found colors
            else:
                color = 'red'   # Red for missing colors

            # Draw sampling point
            draw.ellipse([x-3, y-3, x+3, y+3], fill=color, outline='white')

            # Draw level number
            draw.text((x+5, y-5), str(debug_info['level']), fill='white')

        # Save debug image
        debug_img.save("sampling_points_debug.png")
        print("Debug visualization saved to sampling_points_debug.png")

def generate_html_preview(sampled_colors, sampling_debug):
    """
    Generate HTML preview of all sampled colors
    """
    print("Generating HTML preview...")

    # Find gray colors for segments where no color was found
    gray_colors = {}
    for debug_info in sampling_debug:
        trait = debug_info['trait']
        level = debug_info['level']

        if not debug_info['chosen']:  # No color found
            # Get the gray color for preview
            if 'colors_found' in debug_info:
                for img_key, color_info in debug_info['colors_found'].items():
                    if color_info and color_info['is_gray']:
                        if trait not in gray_colors:
                            gray_colors[trait] = {}
                        gray_colors[trait][str(level)] = color_info['hex']
                        break

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Directly Sampled Autism Wheel Colors</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; text-align: center; }}
        .summary {{ background: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background: #f0f0f0; font-weight: bold; }}
        .color-cell {{ position: relative; }}
        .color-box {{ width: 80px; height: 40px; margin: 5px auto; border: 2px solid #333; border-radius: 4px; }}
        .color-info {{ font-family: monospace; font-size: 11px; margin-top: 5px; }}
        .null-color {{ background: repeating-linear-gradient(45deg, #f0f0f0, #f0f0f0 10px, #e0e0e0 10px, #e0e0e0 20px); }}
        .trait-name {{ font-weight: bold; background: #f8f9fa; }}
        .level-header {{ background: #e9ecef; font-weight: bold; }}
        .missing {{ color: #dc3545; }}
        .found {{ color: #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Directly Sampled Autism Wheel Colors</h1>
        <div class="summary">
            <h3>Sampling Methodology</h3>
            <ul>
                <li><strong>Direct pixel sampling</strong> from "Wheel of Autism 2.png" and "Wheel of Autism 3.png"</li>
                <li><strong>No interpolation or generation</strong> - only actual pixels from images</li>
                <li><strong>OR Logic:</strong> Use colored pixel if found in either image</li>
                <li><strong>Gray Detection:</strong> RGB differences < 25 = gray (inactive)</li>
                <li><strong>Missing Colors:</strong> Shown as null where only gray pixels found</li>
            </ul>
        </div>

        <table>
            <tr>
                <th rowspan="2">Trait</th>
                <th colspan="5">Intensity Levels (Center → Edge)</th>
            </tr>
            <tr>
                <td class="level-header">Level 1<br>(Lightest)</td>
                <td class="level-header">Level 2</td>
                <td class="level-header">Level 3</td>
                <td class="level-header">Level 4</td>
                <td class="level-header">Level 5<br>(Most Intense)</td>
            </tr>
"""

    # Count colors found
    colors_found = 0
    total_colors = 0

    for trait, levels in sampled_colors.items():
        html_content += f'            <tr><td class="trait-name">{trait}</td>'

        for level in range(1, 6):
            level_str = str(level)
            total_colors += 1
            color = levels.get(level_str)

            if color:  # Color found
                colors_found += 1
                html_content += f'''
                <td class="color-cell">
                    <div class="color-box" style="background-color: {color};"></div>
                    <div class="color-info found">{color}</div>
                </td>'''
            else:  # No color found - show gray if available
                gray_color = gray_colors.get(trait, {}).get(level_str, "#c0c0c0")
                html_content += f'''
                <td class="color-cell">
                    <div class="color-box null-color" style="background-color: {gray_color};"></div>
                    <div class="color-info missing">null<br><small>(gray: {gray_color})</small></div>
                </td>'''

        html_content += '</tr>\n'

    html_content += f"""
        </table>

        <div class="summary">
            <h3>Results Summary</h3>
            <p><strong>Colors Found:</strong> <span class="found">{colors_found}/{total_colors}</span> segments have non-gray colors</p>
            <p><strong>Missing:</strong> <span class="missing">{total_colors - colors_found}</span> segments only contain gray pixels</p>
            <p><strong>Sampling Method:</strong> Direct pixel sampling at segment midpoints</p>
            <p><strong>Gray pixels are shown for preview but marked as null in JSON output</strong></p>
        </div>
    </div>
</body>
</html>"""

    with open("sampled_colors_preview.html", "w") as f:
        f.write(html_content)

    print("HTML preview saved to sampled_colors_preview.html")
    return colors_found, total_colors

def main():
    """
    Main function to run direct pixel sampling
    """
    print("Starting direct pixel sampling...")

    # Sample colors from images
    sampled_colors, sampling_debug = sample_colors_from_images()

    if not sampled_colors:
        print("ERROR: Could not sample colors")
        return

    # Save JSON output
    output_file = "wheel_colors_sampled.json"
    with open(output_file, "w") as f:
        json.dump(sampled_colors, f, indent=2)

    print(f"\n✓ Sampled colors saved to {output_file}")

    # Create debug visualization
    create_debug_visualization(sampling_debug)

    # Generate HTML preview
    colors_found, total_colors = generate_html_preview(sampled_colors, sampling_debug)

    # Final summary
    print(f"\n=== DIRECT SAMPLING COMPLETE ===")
    print(f"Colors found: {colors_found}/{total_colors}")
    print(f"JSON output: {output_file}")
    print(f"Preview: sampled_colors_preview.html")
    print(f"Debug: sampling_points_debug.png")

if __name__ == "__main__":
    main()