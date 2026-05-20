const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

/**
 * Create a .skill package file
 * Usage: node create-skill-package.js <skill-path>
 */

const skillPath = process.argv[2];
if (!skillPath) {
    console.error('Usage: node create-skill-package.js <skill-path>');
    process.exit(1);
}

const skillName = path.basename(skillPath);
const outputPath = path.join(path.dirname(skillPath), `${skillName}.skill`);

// Create a write stream
const output = fs.createWriteStream(outputPath);
const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
});

output.on('close', () => {
    console.log(`✓ Skill package created: ${outputPath}`);
    console.log(`  Total size: ${archive.pointer()} bytes`);
});

archive.on('error', (err) => {
    throw err;
});

// Pipe archive data to the file
archive.pipe(output);

// Recursively add all files from the skill directory
archive.directory(skillPath, skillName);

// Finalize the archive
archive.finalize();
