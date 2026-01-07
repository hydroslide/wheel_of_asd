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
const path = require('path');

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

        const traitsData = JSON.parse(fs.readFileSync(TRAITS_JSON_PATH, 'utf8'));
        console.log(`✅ Loaded ${traitsData.length} traits from JSON file`);

        console.log('🔄 Reading HTML file...');

        // Read the HTML file
        if (!fs.existsSync(HTML_FILE_PATH)) {
            throw new Error(`HTML file not found: ${HTML_FILE_PATH}`);
        }

        let htmlContent = fs.readFileSync(HTML_FILE_PATH, 'utf8');

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