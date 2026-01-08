# [Interactive Autism Wheel](https://hydroslide.github.io/wheel_of_asd/)

This app is an interactive HTML-based autism assessment wheel with hover tooltips that provide detailed information about each trait and intensity level. It is designed to be utilized by a teen or a parent to help better understand their unique autism "fingerprint" and maybe determine what level of support they require.

The autism "spectrum" is a pretty bad misnomer and even worse visualization. It conjurs an image of a one dimensional linear spectrum and anyone who knows someone on the spectrum is aware that it is anything but one dimesional.

This wheel is based on the one found in this [great documentary](https://youtu.be/E-yaxqDsfgY?si=vk5i5_Vcwte5e8VR) by [Be Smart](https://www.youtube.com/@besmart). The whole video is worth watching, but you can jump directly to the wheel of autism [here](https://youtu.be/E-yaxqDsfgY?si=vI0wz5dbqkJNdyzC&t=131).

You can access the interactive wheel [here](https://hydroslide.github.io/wheel_of_asd/).

## Features

- **12 Autism Traits**: Visual wheel divided into 12 slices representing different autism characteristics
- **5 Intensity Levels**: Each trait has 5 radial segments representing different intensity levels
- **Interactive Fill**: Click and drag to adjust intensity levels for each trait
- **Rich Tooltips**: Hover over trait names or segments to see detailed definitions and examples
- **Beautiful Gradients**: Colors fade from white (inner) to full saturation (outer) for active segments
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Files

- `index.html` - Main interactive wheel application
- `references/traits.json` - Trait definitions and examples data
- `embed-traits.js` - Script to embed JSON data into HTML (solves CORS issues)
- `package.json` - Node.js project configuration

## Usage

### Opening the Wheel

Simply open `index.html` in any modern web browser. The tooltips should work immediately.

### Updating Trait Data

If you want to modify the trait definitions or examples:

1. **Edit the JSON file**: Modify `references/traits.json` with your changes
2. **Run the embed script**:
   ```bash
   node embed-traits.js
   # OR
   npm run update
   ```
3. **Reload the HTML**: Refresh `index.html` in your browser

The embed script automatically updates the HTML file with the latest JSON data, ensuring tooltips work without CORS issues when opening the file directly.

### Interacting with the Wheel

- **Hover over trait names** (outside the wheel) to see trait definitions
- **Hover over colored segments** to see level-specific examples
- **Click and drag** within segments to adjust intensity levels (0-5)
- **Colored outlines** appear when hovering over segments

## Technical Details

### Why the Embed Script?

Modern browsers block loading local JSON files via JavaScript due to CORS (Cross-Origin Resource Sharing) security policies. The embed script solves this by directly embedding the trait data into the HTML file as a JavaScript variable.

### Tooltip System

- **Smart positioning**: Tooltips automatically reposition to stay within viewport
- **Timing controls**: 300ms delay before showing, 100ms before hiding
- **Responsive**: Tooltip size adjusts for different screen sizes
- **No conflicts**: Tooltips disabled during drag interactions

### Color System

- **Active segments**: Fade from white (inner) to full color saturation (outer)
- **Inactive segments**: Gradient from white (inner) to medium gray (outer)
- **Hover effects**: Full-saturation colored outlines
- **12 unique colors**: Each trait has its own distinct color palette

## Browser Compatibility

Works in all modern browsers:
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Customization

### Modifying Colors

Edit the `SLICE_COLORS` array in `index.html` to change the color palette.

### Adding/Removing Traits

1. Update the `WHEEL_LABELS` array in `index.html`
2. Update `references/traits.json` with corresponding data
3. Run the embed script to update the HTML

### Styling

Modify the CSS styles in the `<style>` section of `index.html` to customize appearance.

## Development

This is a single-file HTML application with embedded JavaScript and CSS. No build process or dependencies are required beyond Node.js for the embed script.

## Use Disclaimer

**IMPORTANT: PLEASE READ THIS DISCLAIMER CAREFULLY BEFORE USING THIS TOOL**

### Relationship to MIT License

This software is distributed under the MIT License (see [LICENSE](LICENSE) file), which grants you broad rights to use, copy, modify, merge, publish, distribute, sublicense, and sell the software. This use disclaimer is **supplementary to and does not modify** the MIT License. Your rights under the MIT License remain unchanged. This disclaimer provides additional important guidance and protections specific to the nature and appropriate use of this particular application.

### Educational and Experimental Tool

This Interactive Autism Wheel (the "Tool") is an experimental educational resource created for informational and educational purposes. The Tool provides general information about autism spectrum characteristics for learning and awareness purposes.

### Not a Medical or Diagnostic Instrument

**CRITICAL MEDICAL DISCLAIMER**: This Tool is **NOT** an official, validated, or approved method for diagnosing autism spectrum disorder or any other medical condition. The Tool does not constitute medical advice, professional diagnosis, treatment, or intervention of any kind. The trait levels, descriptions, and assessment criteria contained herein have not been clinically validated, professionally calibrated, or subjected to peer review.

### Creator Qualifications and Data Sources

This Tool was **NOT** created by licensed medical professionals, autism specialists, psychologists, psychiatrists, or other qualified healthcare practitioners. The information, trait descriptions, and assessment criteria are compiled from publicly available internet sources and the creator's personal experience as the parent of a teenager on the autism spectrum. No professional medical expertise was involved in the development of this Tool.

### Additional Warranties and Liability (Supplementary to MIT License)

**In addition to** the warranty disclaimers and liability limitations provided in the MIT License, the creators specifically disclaim any warranties regarding the medical accuracy, clinical validity, diagnostic reliability, or therapeutic value of the content and assessments provided by this Tool.

**Beyond** the general software liability limitations in the MIT License, users specifically assume all risk related to any medical, diagnostic, or therapeutic reliance on this Tool. Any such reliance is entirely at the user's sole discretion and risk.

### Additional Assumption of Risk and Release (Medical/Diagnostic Risks)

**Regarding medical and diagnostic use specifically**, you expressly assume all risks associated with any medical or diagnostic reliance on this Tool and release and waive any claims against the creators, contributors, and distributors arising from such medical or diagnostic use or reliance.

### Professional Medical Care

**SEEK PROFESSIONAL MEDICAL ADVICE**: This Tool is not intended to replace professional medical consultation, diagnosis, or treatment. If you have concerns about autism spectrum disorder or related conditions for yourself or others, please consult with qualified healthcare professionals, licensed psychologists, developmental specialists, or other appropriate medical practitioners.

### Additional Indemnification (Medical/Diagnostic Claims)

**In addition to** your rights and obligations under the MIT License, you agree to indemnify, defend, and hold harmless the creators, contributors, and distributors from and against any claims, damages, losses, costs, and expenses (including reasonable attorneys' fees) arising specifically from medical or diagnostic use or reliance on this Tool, or from any representation that this Tool constitutes professional medical or diagnostic services.

### Governing Law

This disclaimer shall be governed by and construed in accordance with applicable local laws, consistent with the MIT License terms.

**BY USING THIS TOOL, YOU ACKNOWLEDGE THAT YOU HAVE READ AND UNDERSTOOD THIS DISCLAIMER AND THE MIT LICENSE, AND AGREE THAT BOTH APPLY TO YOUR USE OF THIS SOFTWARE.**