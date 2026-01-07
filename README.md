# Interactive Autism Wheel

An interactive HTML-based autism assessment wheel with hover tooltips that provide detailed information about each trait and intensity level.

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