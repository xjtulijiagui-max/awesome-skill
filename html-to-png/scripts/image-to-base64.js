#!/usr/bin/env node

/**
 * Image to Base64 Converter
 *
 * Usage:
 *   node image-to-base64.js <image-path> [image-type]
 *
 * Examples:
 *   node image-to-base64.js ./photo.png
 *   node image-to-base64.js ./photo.jpg jpeg
 *
 * Outputs a base64 data URL that can be directly used in HTML <img> tags.
 */

const fs = require('fs');
const path = require('path');

function imageToBase64(imagePath, explicitType = null) {
    try {
        // Resolve file path
        const resolvedPath = path.resolve(imagePath);

        // Check if file exists
        if (!fs.existsSync(resolvedPath)) {
            console.error(`Error: File not found: ${imagePath}`);
            process.exit(1);
        }

        // Get file extension for MIME type
        const ext = explicitType || path.extname(resolvedPath).slice(1).toLowerCase();

        // Map extensions to MIME types
        const mimeTypes = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'svg': 'image/svg+xml',
            'bmp': 'image/bmp',
            'ico': 'image/x-icon'
        };

        const mimeType = mimeTypes[ext] || 'image/png';

        // Read file and convert to base64
        const imageBuffer = fs.readFileSync(resolvedPath);
        const base64Data = imageBuffer.toString('base64');

        // Create data URL
        const dataUrl = `data:${mimeType};base64,${base64Data}`;

        // Output
        console.log(dataUrl);

        // Also output file info
        const fileSizeKB = (imageBuffer.length / 1024).toFixed(2);
        console.error(`\nConverted: ${path.basename(resolvedPath)}`);
        console.error(`Size: ${fileSizeKB} KB`);
        console.error(`Type: ${mimeType}`);
        console.error(`Base64 length: ${base64Data.length} characters`);

    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length === 0) {
    console.error('Usage: node image-to-base64.js <image-path> [image-type]');
    console.error('Example: node image-to-base64.js ./photo.png');
    process.exit(1);
}

const imagePath = args[0];
const imageType = args[1] || null;

imageToBase64(imagePath, imageType);
