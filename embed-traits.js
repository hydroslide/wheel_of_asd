#!/usr/bin/env node

/**
 * Embed Traits Data Script
 *
 * This script reads the traits.json file and embeds the data directly into the HTML file,
 * replacing the existing embedded data. This solves CORS issues when opening the HTML
 * file directly in a browser.
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

        // Extract WHEEL_LABELS order from HTML file
        console.log('🔄 Extracting wheel labels order from HTML...');
        const wheelLabelsMatch = htmlContent.match(/const WHEEL_LABELS = \[([\s\S]*?)\];/);
        if (!wheelLabelsMatch) {
            throw new Error('Could not find WHEEL_LABELS array in HTML file');
        }

        const wheelLabelsText = wheelLabelsMatch[1];
        const wheelLabels = wheelLabelsText
            .split(',')
            .map(label => label.trim().replace(/['"`]/g, ''))
            .filter(label => label.length > 0);

        console.log(`✅ Found ${wheelLabels.length} wheel labels`);
        console.log('📋 Wheel order:', wheelLabels.map(label => `"${label}"`).join(', '));

        // Reorder traits data to match WHEEL_LABELS order
        console.log('🔄 Reordering traits data to match wheel labels...');
        const traitsData = [];
        const traitsMap = new Map();

        // Create a map for quick lookup
        traitsDataRaw.forEach(trait => {
            traitsMap.set(trait.trait.toUpperCase(), trait);
        });

        // Reorder according to WHEEL_LABELS
        wheelLabels.forEach(label => {
            const trait = traitsMap.get(label);
            if (!trait) {
                throw new Error(`Could not find trait data for wheel label: "${label}"`);
            }
            traitsData.push(trait);
        });

        console.log(`✅ Reordered ${traitsData.length} traits to match wheel labels order`);

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

        // Create the new embedded data section
        const indentation = '        '; // 8 spaces to match existing indentation
        const formattedTraitsData = JSON.stringify(traitsData, null, 2)
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
        console.log('🎯 Tooltips should now work when opening the HTML file directly in a browser');

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

// Run the script
console.log('🚀 Starting traits data embedding...');
embedTraitsData();