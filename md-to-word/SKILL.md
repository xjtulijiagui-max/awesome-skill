# Convert Markdown to Word Document

Convert markdown files to professionally formatted Word documents with book-style formatting.

## When to use
- When you need to convert Markdown files to Word (.docx) format
- When creating professional documents with headers, page numbers, and table of contents
- When compiling multiple markdown chapters into a single document

## What this skill does

### Input Parameters
- **Source directory**: Path to folder containing markdown files (e.g., `chapters/`)
- **Output file**: Path for the generated Word document (e.g., `output.docx`)

### Features
1. **Read all markdown files** from the source directory
2. **Convert to Word** using Node.js with the `docx` library
3. **Apply book-style formatting**:
   - Professional headers for each section
   - Page numbers in footer
   - Table of contents
   - Proper heading hierarchy (H1, H2, H3)
   - Clean paragraph formatting
4. **Verify completion**: Confirm all chapters included and file created successfully

## Implementation

### Prerequisites
```bash
npm install docx
```

### Script Structure
```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Header, Footer, PageNumber, TableOfContents } = require("docx");
const fs = require("fs");
const path = require("path");

// Read all .md files from source directory
// Parse markdown content
// Create Word document with:
//   - Title page
//   - Table of contents
//   - Chapters with proper headings
//   - Page numbers
//   - Headers
// Write to output file
```

## Usage Example

```
/md-to-word chapters/ my-book.docx
```

This will:
1. Read all `*.md` files from `chapters/` directory
2. Convert them to a formatted Word document
3. Save as `my-book.docx`
4. Confirm completion with chapter count and file size

## Notes
- Files are processed in alphabetical order
- Supports standard Markdown syntax (headers, bold, italic, lists, code blocks)
- Page size: A4 (210mm x 297mm)
- Margins: 2.54cm (1 inch) on all sides
- Font: Calibri 11pt for body, 16pt for H1, 14pt for H2, 12pt for H3
