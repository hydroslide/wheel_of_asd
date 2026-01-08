#!/usr/bin/env python3
"""
Color Palette Validation Tool
Validates the final extracted color palette
"""

import json
import os

def validate_color_palette(json_file):
    """
    Validate the completeness and accuracy of the color palette
    """
    print(f"=== Validating Color Palette: {json_file} ===")

    if not os.path.exists(json_file):
        print(f"ERROR: File not found: {json_file}")
        return False

    with open(json_file, 'r') as f:
        data = json.load(f)

    # Expected traits
    expected_traits = [
        "Sensory Processing", "Emotional Regulation", "Social Interaction",
        "Speech", "Sensory Sensitivities", "Nonverbal Communication",
        "Perception", "Executive Functions", "Intense Interests",
        "Cognitive Flexibility", "Repetitive Behaviors", "Motor Skills/Coordination"
    ]

    print(f"\n1. Checking trait completeness:")
    missing_traits = []
    for trait in expected_traits:
        if trait in data:
            print(f"   ✓ {trait}")
        else:
            print(f"   ✗ {trait} - MISSING")
            missing_traits.append(trait)

    print(f"\n2. Checking level completeness:")
    incomplete_traits = []
    for trait, levels in data.items():
        expected_levels = ["1", "2", "3", "4", "5"]
        missing_levels = []

        for level in expected_levels:
            if level not in levels:
                missing_levels.append(level)

        if missing_levels:
            print(f"   ✗ {trait} - Missing levels: {missing_levels}")
            incomplete_traits.append(trait)
        else:
            print(f"   ✓ {trait} - All 5 levels present")

    print(f"\n3. Checking color validity:")
    invalid_colors = []
    for trait, levels in data.items():
        for level, color in levels.items():
            # Check hex format
            if not color.startswith('#') or len(color) != 7:
                print(f"   ✗ {trait} L{level}: Invalid hex format '{color}'")
                invalid_colors.append((trait, level, color))
            else:
                # Check if it's a valid hex color
                try:
                    int(color[1:], 16)
                    print(f"   ✓ {trait} L{level}: {color}")
                except ValueError:
                    print(f"   ✗ {trait} L{level}: Invalid hex value '{color}'")
                    invalid_colors.append((trait, level, color))

    print(f"\n4. Checking intensity progression:")
    progression_issues = []
    for trait, levels in data.items():
        # Check that colors generally get more intense (darker/more saturated)
        # This is a simplified check - real validation would be more sophisticated
        hex_colors = [levels.get(str(i), "#000000") for i in range(1, 6)]

        # Convert to brightness values for basic progression check
        brightness_values = []
        for hex_color in hex_colors:
            if hex_color.startswith('#') and len(hex_color) == 7:
                try:
                    r = int(hex_color[1:3], 16)
                    g = int(hex_color[3:5], 16)
                    b = int(hex_color[5:7], 16)
                    brightness = (r + g + b) / 3
                    brightness_values.append(brightness)
                except:
                    brightness_values.append(0)
            else:
                brightness_values.append(0)

        # Generally, level 1 should be lighter than level 5 (with some exceptions)
        if len(brightness_values) == 5:
            if brightness_values[0] < brightness_values[4]:
                progression_issues.append(f"{trait}: L1 darker than L5")
            else:
                print(f"   ✓ {trait}: Good progression (L1={brightness_values[0]:.0f} → L5={brightness_values[4]:.0f})")

    # Summary
    print(f"\n=== VALIDATION SUMMARY ===")
    total_traits = len(expected_traits)
    total_levels = total_traits * 5

    print(f"Traits: {total_traits - len(missing_traits)}/{total_traits} complete")
    print(f"Levels: {total_levels - len(incomplete_traits) * 5}/{total_levels} complete")
    print(f"Valid colors: {total_levels - len(invalid_colors)}/{total_levels}")

    if progression_issues:
        print(f"Progression issues: {len(progression_issues)}")
        for issue in progression_issues:
            print(f"  - {issue}")

    # Overall validation
    is_valid = (len(missing_traits) == 0 and
                len(incomplete_traits) == 0 and
                len(invalid_colors) == 0)

    if is_valid:
        print(f"\n🎉 VALIDATION PASSED: Complete color palette with all 60 hex values!")
    else:
        print(f"\n⚠️  VALIDATION ISSUES FOUND")

    return is_valid

def create_color_preview_html(json_file, output_file):
    """
    Create an HTML preview of the color palette
    """
    if not os.path.exists(json_file):
        return

    with open(json_file, 'r') as f:
        data = json.load(f)

    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Autism Wheel Color Palette</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .trait { margin: 20px 0; }
        .trait-name { font-weight: bold; margin-bottom: 10px; }
        .color-row { display: flex; align-items: center; margin: 5px 0; }
        .color-box { width: 60px; height: 30px; margin-right: 10px; border: 1px solid #ccc; }
        .color-info { font-family: monospace; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Autism Wheel Color Palette</h1>
    <p>Complete color palette with 60 hex values for the 12 autism traits, each with 5 intensity levels.</p>

    <table>
        <tr>
            <th>Trait</th>
            <th>Level 1 (Lightest)</th>
            <th>Level 2</th>
            <th>Level 3</th>
            <th>Level 4</th>
            <th>Level 5 (Most Intense)</th>
        </tr>
"""

    for trait, levels in data.items():
        html_content += f'        <tr><td><strong>{trait}</strong></td>'
        for level in range(1, 6):
            color = levels.get(str(level), "#ffffff")
            html_content += f'<td><div style="background-color: {color}; width: 80px; height: 30px; margin: auto; border: 1px solid #ccc;"></div><br><small>{color}</small></td>'
        html_content += '</tr>\n'

    html_content += """
    </table>

    <h2>Individual Trait Details</h2>
"""

    for trait, levels in data.items():
        html_content += f'    <div class="trait"><div class="trait-name">{trait}</div>\n'
        for level in range(1, 6):
            color = levels.get(str(level), "#ffffff")
            html_content += f'        <div class="color-row"><div class="color-box" style="background-color: {color};"></div><span class="color-info">Level {level}: {color}</span></div>\n'
        html_content += '    </div>\n'

    html_content += """
</body>
</html>"""

    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"Color preview saved to {output_file}")

def main():
    """
    Run validation on the final color palette
    """
    json_file = "final_wheel_colors.json"

    # Validate the palette
    is_valid = validate_color_palette(json_file)

    # Create HTML preview
    create_color_preview_html(json_file, "color_palette_preview.html")

    return is_valid

if __name__ == "__main__":
    main()