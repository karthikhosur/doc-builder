# LaTeX Document Generator - Folder-Based Usage Guide

## Overview

This LaTeX generator allows you to create professional documents by organizing them in folders with their own templates, data, and resources. Each folder represents a document type (invoices, letters, reports, etc.) and contains everything needed to generate that specific document.

## Font Configuration

The system uses **Arial font** as the default for all documents, providing a professional and modern appearance.

### Font Settings
- **Main Font**: Arial (via `fontspec` package)
- **Fallback**: System will automatically use available fonts if Arial is not installed
- **Supported**: All standard font weights (regular, bold, italic, bold-italic)

### Customizing Fonts
To change the font in any template, modify the font specification:

```latex
\usepackage{fontspec}
\setmainfont{Arial}              % For Arial
\setmainfont{Helvetica}          % For Helvetica
\setmainfont{Times New Roman}    % For Times New Roman
\setmainfont{Calibri}            % For Calibri
```

### Font Requirements
- Requires `fontspec` package (already included)
- Works with Tectonic LaTeX engine
- System fonts must be installed on the machine

## Quick Start

### 1. Basic Usage

```bash
# Generate PDF from JSON file (looks for template.tex in same folder)
python latex_generator.py data.json

# Or make it executable and run directly
chmod +x latex_generator.py
./latex_generator.py data.json
```

### 2. Command Line Options

```bash
# Generate PDF with custom template name
python latex_generator.py data.json -t invoice_template.tex

# Generate PDF with custom output directory
python latex_generator.py data.json -o ./output/

# List available components
python latex_generator.py --list-components

# Enable verbose logging
python latex_generator.py data.json -v

# Suppress all output except errors
python latex_generator.py data.json -q
```

## Folder Structure

### Recommended Organization

```
doc-builder/
├── latex_generator.py           # Main generator script
├── components/                  # Global reusable components
│   ├── table_basic.tex
│   ├── header_company.tex
│   └── ...
├── invoices/                    # Invoice documents
│   ├── data.json               # Invoice data
│   ├── template.tex            # Invoice template
│   └── resources/              # Images, logos, etc.
├── reports/                     # Report documents
│   ├── data.json               # Report data
│   ├── template.tex            # Report template
│   └── resources/              # Charts, graphs, etc.
└── letters/                     # Letter documents
    ├── data.json               # Letter data
    ├── template.tex            # Letter template
    └── resources/              # Letterhead, signatures, etc.
```

### Key Benefits

1. **Organized**: Each document type has its own folder
2. **Self-contained**: All resources are in one place
3. **Flexible**: Use any template name with `-t` option
4. **Reusable**: Components work across all document types

## Example Usage

### Invoice Generation

```bash
# Generate invoice PDF
python latex_generator.py invoices/data.json

# Output: invoices/data.pdf
```

**File Structure:**
```
invoices/
├── data.json          # Invoice data (items, client info, etc.)
├── template.tex       # Invoice template with components
└── resources/         # Company logo, signature, etc.
```

### Report Generation

```bash
# Generate quarterly report
python latex_generator.py reports/data.json

# Output: reports/data.pdf
```

**File Structure:**
```
reports/
├── data.json          # Report data (metrics, sections, etc.)
├── template.tex       # Report template with tables/charts
└── resources/         # Charts, graphs, logos, etc.
```

### Letter Generation

```bash
# Generate business letter
python latex_generator.py letters/data.json

# Output: letters/data.pdf
```

**File Structure:**
```
letters/
├── data.json          # Letter data (sender, recipient, content)
├── template.tex       # Letter template with components
└── resources/         # Letterhead, signatures, etc.
```

## Creating New Document Types

### 1. Create Folder Structure

```bash
mkdir -p contracts/resources
```

### 2. Create Template (`contracts/template.tex`)

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{tcolorbox}
\usepackage{graphicx}
\geometry{margin=1in}

\begin{document}

% Use components
\VAR{component('header_company', 
    company_name=company.name,
    address=company.address,
    phone=company.phone,
    email=company.email,
    date=contract.date
)}

\begin{center}
    {\LARGE \textbf{\VAR{contract.title}}}
\end{center}

% Contract content
\VAR{contract.content}

% Signature blocks
\VAR{component('signature_block', 
    name=party1.name,
    title=party1.title,
    date=contract.date
)}

\end{document}
```

### 3. Create Data (`contracts/data.json`)

```json
{
  "company": {
    "name": "Legal Services Corp",
    "address": "123 Law Street",
    "phone": "(555) 123-4567",
    "email": "contracts@legalservices.com"
  },
  "contract": {
    "title": "Service Agreement",
    "date": "2024-01-15",
    "content": "This agreement outlines..."
  },
  "party1": {
    "name": "John Doe",
    "title": "Legal Director"
  }
}
```

### 4. Generate PDF

```bash
python latex_generator.py contracts/data.json
```

## Advanced Features

### Custom Template Names

```bash
# Use a specific template
python latex_generator.py invoices/data.json -t detailed_invoice.tex
```

### Custom Output Directory

```bash
# Output to different location
python latex_generator.py invoices/data.json -o ./final_documents/
```

### Component Management

```bash
# List all available components
python latex_generator.py --list-components

# Output:
# Available components:
#   - signature_block
#   - table_professional
#   - header_company
#   - section_box
#   - bullet_list
#   - numbered_list
#   - contact_info
#   - quote
```

## Working with Components

### Using Components in Templates

```latex
% Basic component usage
\VAR{component('bullet_list', 
    items=['Item 1', 'Item 2', 'Item 3']
)}

% Component with parameters
\VAR{component('table_professional', 
    headers=['Name', 'Role', 'Email'],
    rows=[
        ['John Doe', 'Manager', 'john@company.com'],
        ['Jane Smith', 'Developer', 'jane@company.com']
    ],
    title='Team Members'
)}

% Component with conditional parameters
\VAR{component('header_company', 
    company_name=company.name,
    address=company.address,
    phone=company.phone,
    email=company.email,
    logo_path=company.logo if company.logo else None,
    date=document.date
)}
```

### Available Components

- **table_basic**: Simple table with borders
- **table_professional**: Professional table with booktabs
- **header_company**: Company header with logo and contact info
- **section_box**: Colored highlight boxes
- **signature_block**: Signature blocks with dates
- **bullet_list**: Bullet point lists
- **numbered_list**: Numbered lists
- **contact_info**: Formatted contact information
- **quote**: Formatted quotations

## Tips and Best Practices

### 1. Data Organization

- Keep related data in the same JSON file
- Use nested objects for logical grouping
- Use meaningful key names

### 2. Template Design

- Start with simple templates and add complexity gradually
- Use comments to document template sections
- Test templates with sample data first

### 3. Resource Management

- Store images in the `resources/` folder within each document folder
- Use relative paths for images: `resources/logo.png`
- Keep resource files organized by type

### 4. Version Control

- Use descriptive filenames for templates
- Keep templates and data in version control
- Document changes in template files

## Troubleshooting

### Common Issues

1. **Template not found**: Make sure `template.tex` exists in the same folder as your JSON file
2. **Component errors**: Check that component names are spelled correctly
3. **LaTeX compilation errors**: Check the generated `.tex` file for syntax errors
4. **Missing resources**: Ensure image paths are correct and files exist

### Debug Mode

```bash
# Enable verbose logging to see detailed information
python latex_generator.py data.json -v
```

### Error Messages

- `❌ File not found`: Check that the JSON file path is correct
- `❌ Template not found`: Ensure template.tex exists in the same folder
- `❌ PDF compilation failed`: Check LaTeX syntax and required packages

## Examples Included

The repository includes three complete examples:

1. **invoices/**: Professional invoice template with itemized billing
2. **reports/**: Quarterly report template with data tables
3. **letters/**: Business letter template with components

Try them out:

```bash
python latex_generator.py invoices/data.json
python latex_generator.py reports/data.json
python latex_generator.py letters/data.json
```

## Next Steps

1. **Customize existing templates** to match your branding
2. **Create new document types** following the folder structure
3. **Add custom components** for specialized layouts
4. **Integrate with your workflow** using command-line automation

For more information about components, see `COMPONENT_GUIDE.md`. 