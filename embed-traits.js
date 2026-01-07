#!/usr/bin/env node

/**
 * Embed Traits Data Script (Order-Independent)
 *
 * This script reads the traits.json file and embeds the data directly into the HTML file,
 * replacing the existing embedded data. This solves CORS issues when opening the HTML
 * file directly in a browser.
 *
 * The script validates that all trait IDs referenced in WHEEL_CONFIG exist in the JSON data,
 * but does NOT reorder the data - the wheel uses ID-based lookups for robustness.
 *
 * Usage: node embed-traits.js
 */

const fs = require('fs');

// File paths
const TRAITS_JSON_PATH = './references/traits.json';
const HTML_FILE_PATH = './index.html';

// Markers to find the embedded data section
const START_MARKER = '// <!-- TRAITS_DATA_START -->';
const END_MARKER = '// <!-- TRAITS_DATA_END -->';

function embedTraitsData() {
    try {
        console.log('🔄 Reading traits.json...');

        // Read and parse the traits JSON file
        if (!fs.existsSync(TRAITS_JSON_PATH)) {
            throw new Error(`Traits file not found: ${TRAITS_JSON_PATH}`);
        }

        const traitsDataRaw = JSON.parse(fs.readFileSync(TRAITS_JSON_PATH, 'utf8'));
        console.log(`✅ Loaded ${traitsDataRaw.length} traits from JSON file`);

        console.log('🔄 Reading HTML file...');

        // Read the HTML file
        if (!fs.existsSync(HTML_FILE_PATH)) {
            throw new Error(`HTML file not found: ${HTML_FILE_PATH}`);
        }

        let htmlContent = fs.readFileSync(HTML_FILE_PATH, 'utf8');

        // Extract WHEEL_CONFIG trait IDs from HTML file
        console.log('🔄 Extracting wheel configuration from HTML...');
        const wheelConfigMatch = htmlContent.match(/const WHEEL_CONFIG = \[([\s\S]*?)\];/);
        if (!wheelConfigMatch) {
            throw new Error('Could not find WHEEL_CONFIG array in HTML file');
        }

        // Parse the WHEEL_CONFIG to extract trait IDs
        const wheelConfigText = wheelConfigMatch[1];
        const traitIdMatches = wheelConfigText.match(/traitId: '([^']+)'/g);
        if (!traitIdMatches) {
            throw new Error('Could not extract trait IDs from WHEEL_CONFIG');
        }

        const requiredTraitIds = traitIdMatches.map(match =>
            match.replace(/traitId: '([^']+)'/, '$1')
        );

        console.log(`✅ Found ${requiredTraitIds.length} trait IDs in wheel configuration`);
        console.log('🔧 Required trait IDs:', requiredTraitIds.map(id => `"${id}"`).join(', '));

        // Validate that all required trait IDs exist in the data (ORDER INDEPENDENT!)
        console.log('🔄 Validating trait data completeness...');
        const availableTraitIds = new Set();
        const traitsMap = new Map();

        // Build lookup maps - auto-generate IDs from trait names
        traitsDataRaw.forEach(trait => {
            // Generate ID from trait name (convert to kebab-case)
            const generatedId = trait.trait
                .toLowerCase()
                .replace(/[\/\s]+/g, '-')  // Replace spaces and slashes with dashes
                .replace(/[^a-z0-9-]/g, '') // Remove any other special characters
                .replace(/-+/g, '-')        // Collapse multiple dashes
                .replace(/^-|-$/g, '');     // Remove leading/trailing dashes

            // Add the generated ID to the trait data for embedding
            trait.id = generatedId;

            availableTraitIds.add(generatedId);
            traitsMap.set(generatedId, trait);

            console.log(`✅ Generated ID "${generatedId}" for trait "${trait.trait}"`);
        });

        // Check for missing traits
        const missingTraitIds = requiredTraitIds.filter(id => !availableTraitIds.has(id));
        if (missingTraitIds.length > 0) {
            throw new Error(`Missing trait data for IDs: ${missingTraitIds.map(id => `"${id}"`).join(', ')}`);
        }

        // Check for extra traits (not required, just informational)
        const extraTraitIds = Array.from(availableTraitIds).filter(id => !requiredTraitIds.includes(id));
        if (extraTraitIds.length > 0) {
            console.log('ℹ️  Extra traits (not used by wheel):', extraTraitIds.map(id => `"${id}"`).join(', '));
        }

        console.log(`✅ All ${requiredTraitIds.length} required traits found in data`);
        console.log('🎯 Order-independent validation complete - no reordering needed!');

        // Find the start and end markers
        const startIndex = htmlContent.indexOf(START_MARKER);
        const endIndex = htmlContent.indexOf(END_MARKER);

        if (startIndex === -1) {
            throw new Error('Start marker not found in HTML file. Make sure the HTML contains: ' + START_MARKER);
        }

        if (endIndex === -1) {
            throw new Error('End marker not found in HTML file. Make sure the HTML contains: ' + END_MARKER);
        }

        console.log('🔄 Embedding traits data...');

        // Create the new embedded data section (using original order - no reordering needed!)
        const indentation = '        '; // 8 spaces to match existing indentation
        const formattedTraitsData = JSON.stringify(traitsDataRaw, null, 2)
            .split('\n')
            .map((line, index) => {
                // First line doesn't need extra indentation
                if (index === 0) return line;
                // Add proper indentation to subsequent lines
                return indentation + line;
            })
            .join('\n');

        const newDataSection = `${START_MARKER}
        const traitsData = ${formattedTraitsData};
        ${END_MARKER}`;

        // Replace the section between markers
        const beforeSection = htmlContent.substring(0, startIndex);
        const afterSection = htmlContent.substring(endIndex + END_MARKER.length);

        const updatedHtml = beforeSection + newDataSection + afterSection;

        // Write the updated HTML file
        fs.writeFileSync(HTML_FILE_PATH, updatedHtml, 'utf8');

        console.log('✅ Successfully embedded traits data into HTML file');
        console.log('📄 Updated file:', HTML_FILE_PATH);
        console.log('🎯 Order-independent embedding complete - wheel will use ID-based lookups');
        console.log('🌐 Tooltips should now work when opening the HTML file directly in a browser');

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

// Run the script
console.log('🚀 Starting traits data embedding...');
embedTraitsData();