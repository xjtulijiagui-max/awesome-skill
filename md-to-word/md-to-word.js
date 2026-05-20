/**
 * Markdown to Word Converter
 * Converts markdown files to professionally formatted Word documents
 */

const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Header, Footer, PageNumber, TableOfContents, BorderStyle, convertInchesToTwip } = require("docx");
const fs = require("fs");
const path = require("path");

/**
 * Parse markdown content and convert to Word paragraphs
 */
function parseMarkdown(markdown) {
    const lines = markdown.split('\n');
    const paragraphs = [];

    for (const line of lines) {
        const trimmed = line.trim();

        // Empty line
        if (!trimmed) {
            paragraphs.push(new Paragraph({}));
            continue;
        }

        // H1 Heading
        if (trimmed.startsWith('# ')) {
            const text = trimmed.substring(2).trim();
            paragraphs.push(new Paragraph({
                text: text,
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 240, after: 120 },
                alignment: AlignmentType.CENTER
            }));
            continue;
        }

        // H2 Heading
        if (trimmed.startsWith('## ')) {
            const text = trimmed.substring(3).trim();
            paragraphs.push(new Paragraph({
                text: text,
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 100 },
                alignment: AlignmentType.LEFT
            }));
            continue;
        }

        // H3 Heading
        if (trimmed.startsWith('### ')) {
            const text = trimmed.substring(4).trim();
            paragraphs.push(new Paragraph({
                text: text,
                heading: HeadingLevel.HEADING_3,
                spacing: { before: 160, after: 80 }
            }));
            continue;
        }

        // H4 Heading
        if (trimmed.startsWith('#### ')) {
            const text = trimmed.substring(5).trim();
            paragraphs.push(new Paragraph({
                text: text,
                heading: HeadingLevel.HEADING_4,
                spacing: { before: 140, after: 60 }
            }));
            continue;
        }

        // Code block (simple version - inline)
        if (trimmed.startsWith('```')) {
            paragraphs.push(new Paragraph({
                children: [
                    new TextRun({
                        text: trimmed,
                        font: "Consolas",
                        size: 20
                    })
                ],
                spacing: { before: 100, after: 100 }
            }));
            continue;
        }

        // Unordered list
        if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
            const text = trimmed.substring(2).trim();
            paragraphs.push(new Paragraph({
                text: text,
                bullet: { level: 0 },
                spacing: { before: 80, after: 80 }
            }));
            continue;
        }

        // Ordered list (simple - just number at start)
        if (/^\d+\.\s/.test(trimmed)) {
            const match = trimmed.match(/^\d+\.\s(.*)/);
            if (match) {
                paragraphs.push(new Paragraph({
                    text: match[1],
                    numbering: { reference: "numbering", level: 0 },
                    spacing: { before: 80, after: 80 }
                }));
                continue;
            }
        }

        // Bold text **text**
        let processedLine = trimmed;
        const boldRegex = /\*\*(.+?)\*\*/g;
        const textRuns = [];

        let lastIndex = 0;
        let match;
        while ((match = boldRegex.exec(trimmed)) !== null) {
            // Add text before bold
            if (match.index > lastIndex) {
                textRuns.push(new TextRun(trimmed.substring(lastIndex, match.index)));
            }
            // Add bold text
            textRuns.push(new TextRun({ text: match[1], bold: true }));
            lastIndex = match.index + match[0].length;
        }
        // Add remaining text
        if (lastIndex < trimmed.length) {
            textRuns.push(new TextRun(trimmed.substring(lastIndex)));
        }

        // Regular paragraph
        if (textRuns.length > 0) {
            paragraphs.push(new Paragraph({
                children: textRuns,
                spacing: { before: 80, after: 80 },
                indent: { firstLine: convertInchesToTwip(0.5) }
            }));
        } else {
            paragraphs.push(new Paragraph({
                text: trimmed,
                spacing: { before: 80, after: 80 },
                indent: { firstLine: convertInchesToTwip(0.5) }
            }));
        }
    }

    return paragraphs;
}

/**
 * Convert markdown directory to Word document
 */
async function convertMarkdownToWord(sourceDir, outputFile) {
    console.log(`Reading markdown files from: ${sourceDir}`);

    // Check if directory exists
    if (!fs.existsSync(sourceDir)) {
        throw new Error(`Source directory not found: ${sourceDir}`);
    }

    // Read all .md files
    const files = fs.readdirSync(sourceDir)
        .filter(file => file.endsWith('.md'))
        .sort(); // Alphabetical order

    if (files.length === 0) {
        throw new Error(`No markdown files found in: ${sourceDir}`);
    }

    console.log(`Found ${files.length} markdown file(s):`);
    files.forEach(file => console.log(`  - ${file}`));

    // Collect all paragraphs
    const allParagraphs = [];

    // Add title page
    allParagraphs.push(
        new Paragraph({
            text: "Table of Contents",
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER,
            spacing: { before: 400, after: 400 }
        })
    );

    // Add table of contents placeholder
    allParagraphs.push(
        new Paragraph({
            text: "Table of Contents",
            heading: HeadingLevel.HEADING_1
        })
    );

    // Process each file
    for (const file of files) {
        const filePath = path.join(sourceDir, file);
        const content = fs.readFileSync(filePath, 'utf-8');
        const paragraphs = parseMarkdown(content);

        // Add page break between chapters (except first)
        if (allParagraphs.length > 2) {
            allParagraphs.push(
                new Paragraph({
                    children: [],
                    pageBreakBefore: true
                })
            );
        }

        allParagraphs.push(...paragraphs);
    }

    // Create document
    const doc = new Document({
        sections: [{
            properties: {
                page: {
                    margin: {
                        top: convertInchesToTwip(1),
                        right: convertInchesToTwip(1),
                        bottom: convertInchesToTwip(1),
                        left: convertInchesToTwip(1)
                    }
                }
            },
            headers: {
                default: new Header({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({
                                    text: "Generated from Markdown",
                                    size: 20,
                                    color: "666666"
                                })
                            ],
                            alignment: AlignmentType.CENTER,
                            spacing: { after: 200 }
                        })
                    ]
                })
            },
            footers: {
                default: new Footer({
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.CENTER,
                            children: [
                                new TextRun({
                                    children: [PageNumber.CURRENT]
                                })
                            ]
                        })
                    ]
                })
            },
            children: allParagraphs
        }]
    });

    // Write to file
    console.log(`\nGenerating Word document: ${outputFile}`);
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputFile, buffer);

    const stats = fs.statSync(outputFile);
    console.log(`\n✓ Success!`);
    console.log(`  Chapters processed: ${files.length}`);
    console.log(`  Output file: ${outputFile}`);
    console.log(`  File size: ${(stats.size / 1024).toFixed(2)} KB`);
}

// Main execution
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length < 2) {
        console.log('Usage: node md-to-word.js <source-directory> <output-file.docx>');
        console.log('Example: node md-to-word.js chapters/ my-book.docx');
        process.exit(1);
    }

    const [sourceDir, outputFile] = args;

    convertMarkdownToWord(sourceDir, outputFile)
        .then(() => console.log('\n✓ Conversion complete!'))
        .catch(err => {
            console.error('\n✗ Error:', err.message);
            process.exit(1);
        });
}

module.exports = { convertMarkdownToWord, parseMarkdown };
