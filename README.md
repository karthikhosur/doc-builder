# LaTeX Generator

A universal Python tool for populating LaTeX templates with JSON data using Jinja2 templating engine.

## Features

- 🚀 **Universal**: Works with any LaTeX template and JSON data structure
- 🎨 **Flexible**: Supports both template files and string templates
- 🔧 **Customizable**: Custom Jinja2 filters for LaTeX-specific formatting
- 📄 **PDF Generation**: Built-in PDF compilation support
- 🛡️ **Safe**: Automatic LaTeX character escaping
- 📊 **Rich Formatting**: Currency, date, text formatting, and image inclusion filters

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Basic Usage

```python
from latex_generator import LaTeXGenerator

# Initialize generator
generator = LaTeXGenerator(template_dir="templates")

# Generate LaTeX document
latex_content = generator.generate_latex(
    template_name="my_template.tex",
    data="my_data.json",
    output_file="output/document.tex"
)
```

### Using Dictionary Data

```python
# Use dictionary data instead of JSON file
data = {
    "title": "My Document",
    "author": "John Doe",
    "content": "Hello World!"
}

latex_content = generator.generate_latex(
    template_name="my_template.tex",
    data=data,
    output_file="output/document.tex"
)
```

### String Templates

```python
# Use string template instead of file
template_str = r"""
\documentclass{article}
\begin{document}
\title{\VAR{title}}
\author{\VAR{author}}
\maketitle
\VAR{content}
\end{document}
"""

latex_content = generator.generate_from_string_template(
    template_content=template_str,
    data=data,
    output_file="output/document.tex"
)
```

## Template Syntax

The generator uses custom Jinja2 delimiters to avoid conflicts with LaTeX syntax:

| Jinja2 Element | Standard Syntax | LaTeX Generator Syntax |
|----------------|-----------------|------------------------|
| Variables      | `{{ variable }}`| `\VAR{variable}`       |
| Blocks         | `{% block %}`   | `\BLOCK{block}`        |
| Comments       | `{# comment #}` | `\#{comment}`          |
| Line Statements| N/A            | `%% statement`         |

### Template Examples

**Variables:**
```latex
\VAR{company.name}
\VAR{invoice.total|currency}
\VAR{invoice.date|date_format}
```

**Loops:**
```latex
\BLOCK{for item in invoice.items}
\VAR{item.description} & \VAR{item.quantity} & \VAR{item.rate|currency} \\
\BLOCK{endfor}
```

**Conditionals:**
```latex
\BLOCK{if invoice.tax_rate > 0}
\textbf{Tax (\VAR{invoice.tax_rate}\%):} & \VAR{invoice.tax_amount|currency} \\
\BLOCK{endif}
```

## Built-in Filters

### `latex_escape`
Escapes special LaTeX characters in text:
```latex
\VAR{user_input|latex_escape}
```

### `currency`
Formats numbers as currency:
```latex
\VAR{amount|currency}          % $1,234.56
\VAR{amount|currency("€")}     % €1,234.56
```

### `date_format`
Formats date strings:
```latex
\VAR{date|date_format}                    % January 15, 2024
\VAR{date|date_format("%Y-%m-%d")}       % 2024-01-15
```

### `image`
Includes images in LaTeX documents:
```latex
\VAR{image_path|image}                    % Basic image inclusion
\VAR{image_path|image("width=2in")}      % Image with specific width
\VAR{image_path|image("height=3cm")}     % Image with specific height
\VAR{image_path|image("scale=0.8")}      % Scaled image (80%)
\VAR{image_path|image("angle=45")}       % Rotated image (45 degrees)
\VAR{image_path|image("width=3cm", "height=2cm")} % Multiple options
```

## Invoice Example

The repository includes a complete invoice generation example:

### Files Structure
```
├── latex_generator.py                    # Main generator class
├── templates/
│   ├── invoice_template.tex              # Basic invoice template
│   └── invoice_with_images_template.tex  # Enhanced invoice with images
├── images/
│   ├── company_logo.png                  # Sample company logo
│   ├── signature.png                     # Sample signature
│   └── qr_code.png                      # Sample QR code
├── sample_invoice_data.json              # Sample invoice data (with image paths)
├── test_invoice.py                       # Basic test script
├── test_images.py                        # Image functionality test script
├── test_tectonic.py                      # Tectonic speed benchmark script
├── requirements.txt                      # Dependencies
└── README.md                            # This file
```

### Running the Invoice Example

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test
python test_invoice.py
```

This will generate:
- `output/generated_invoice.tex` - The LaTeX file
- `output/generated_invoice.pdf` - The PDF file (if pdflatex is available)

### Running the Image Test

```bash
# Test image functionality
python test_images.py
```

This will generate:
- `output/invoice_with_images.tex` - Invoice with company logo, signature, and QR code
- `output/string_template_with_images.tex` - Simple document with images
- `output/fixed_invoice_with_images.pdf` - PDF with embedded images

### Running the Tectonic Speed Test

```bash
# Benchmark compilation speeds across engines
python test_tectonic.py
```

This will:
- Check which LaTeX engines are available on your system
- Benchmark compilation speed across Tectonic, pdflatex, and xelatex
- Show performance comparisons and speed improvements
- Test Tectonic's automatic package management features

### Sample Invoice Data Structure

```json
{
  "company": {
    "name": "TechSolutions Inc.",
    "address": "123 Business Ave",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94102",
    "phone": "(555) 123-4567",
    "email": "info@techsolutions.com",
    "logo_path": "images/company_logo.png"
  },
  "client": {
    "name": "ABC Corporation",
    "address": "456 Client Street",
    "city": "Los Angeles",
    "state": "CA",
    "zip": "90210",
    "email": "accounting@abccorp.com",
    "phone": "(555) 987-6543"
  },
  "invoice": {
    "number": "INV-2024-001",
    "date": "2024-01-15",
    "due_date": "2024-02-15",
    "items": [
      {
        "description": "Web Development Services",
        "quantity": 40,
        "rate": 125.00
      }
    ],
    "subtotal": 5000.00,
    "tax_rate": 8.25,
    "tax_amount": 412.50,
    "total": 5412.50
  },
  "payment_info": {
    "method": "Bank Transfer",
    "qr_code_path": "images/qr_code.png"
  },
  "signature": {
    "path": "images/signature.png",
    "name": "John Doe",
    "title": "CEO"
  }
}
```

## Working with Images

The LaTeX generator supports embedding images in your documents using the `image` filter.

### Image Filter Usage

```latex
% Basic image inclusion
\VAR{company.logo_path|image}

% Image with specific width
\VAR{company.logo_path|image("width=2in")}

% Image with multiple options
\VAR{signature.path|image("width=3cm", "height=2cm")}

% Conditional image inclusion
\BLOCK{if company.logo_path}
\VAR{company.logo_path|image("width=2in")}\\[0.5cm]
\BLOCK{endif}
```

### Supported Image Formats

- PNG (`.png`) - Recommended for logos and graphics
- JPEG (`.jpg`, `.jpeg`) - Good for photographs  
- PDF (`.pdf`) - Vector graphics
- SVG (`.svg`) - Vector graphics (with additional packages)

### Image Options

| Option | Description | Example |
|--------|-------------|---------|
| `width` | Set image width | `"width=2in"`, `"width=5cm"`, `"width=0.5\\textwidth"` |
| `height` | Set image height | `"height=3cm"`, `"height=0.3\\textheight"` |
| `scale` | Scale image by factor | `"scale=0.8"`, `"scale=1.2"` |
| `angle` | Rotate image | `"angle=45"`, `"angle=90"` |

### Path Considerations

- Use forward slashes `/` for paths (works on all platforms)
- Paths are relative to the LaTeX compilation directory
- For PDF compilation, ensure images are accessible from the output directory

### Example: Enhanced Invoice Template

```latex
% Company header with logo
\begin{center}
\BLOCK{if company.logo_path}
\VAR{company.logo_path|image("width=2in")}\\[0.3cm]
\BLOCK{else}
{\huge\textbf{\VAR{company.name}}}\\[0.5cm]
\BLOCK{endif}
\end{center}

% Payment QR code
\begin{minipage}[t]{0.3\textwidth}
\BLOCK{if payment_info.qr_code_path}
\begin{center}
\VAR{payment_info.qr_code_path|image("width=1.5in")}\\
\textit{\footnotesize Scan for payment}
\end{center}
\BLOCK{endif}
\end{minipage}

% Signature section
\BLOCK{if signature.path}
\VAR{signature.path|image("width=2in")}\\[0.2cm]
\textbf{\VAR{signature.name}}\\
\textit{\VAR{signature.title}}
\BLOCK{endif}
```

## PDF Compilation

The LaTeX generator uses **Tectonic** for ultra-fast, reliable PDF compilation.

### Automatic Compilation
```python
# Compile LaTeX to PDF with Tectonic
success = generator.compile_latex_to_pdf(
    latex_file="output/document.tex",
    output_dir="output"
)
```

### Why Tectonic?

🚀 **Tectonic** is a modern, Rust-based LaTeX engine that's:
- **2-5x faster** than traditional LaTeX engines
- **Automatic package management** - no manual installation needed
- **Reproducible builds** - consistent output across systems
- **Memory safe** - built with Rust for reliability
- **Cross-platform** - works on Windows, macOS, and Linux

### Installing Tectonic

**macOS:**
```bash
brew install tectonic
```

**Windows:**
```bash
winget install TectonicTypesetting.Tectonic
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install tectonic

# Or via Cargo (cross-platform)
cargo install tectonic
```

### Testing Tectonic

Run the test suite to see Tectonic in action:
```bash
python test_tectonic.py
```

This will:
- Test compilation speed with invoices and images
- Demonstrate automatic package management
- Show Tectonic's key benefits

### Manual Compilation
```bash
# Direct Tectonic usage
tectonic document.tex
```

## API Reference

### LaTeXGenerator Class

#### `__init__(template_dir="templates")`
Initialize the generator with a template directory.

#### `generate_latex(template_name, data, output_file=None)`
Generate LaTeX document from template file and data.

- `template_name`: Name of the template file
- `data`: JSON file path or dictionary
- `output_file`: Optional output file path
- Returns: Generated LaTeX content as string

#### `generate_from_string_template(template_content, data, output_file=None)`
Generate LaTeX document from template string and data.

- `template_content`: Template content as string
- `data`: JSON file path or dictionary
- `output_file`: Optional output file path
- Returns: Generated LaTeX content as string

#### `compile_latex_to_pdf(latex_file, output_dir=None)`
Compile LaTeX file to PDF.

- `latex_file`: Path to LaTeX file
- `output_dir`: Optional output directory
- Returns: True if successful, False otherwise

#### `load_json_data(json_file)`
Load JSON data from file.

- `json_file`: Path to JSON file
- Returns: Loaded data as dictionary

## Error Handling

The generator includes comprehensive error handling:

- JSON parsing errors
- Template loading errors
- File I/O errors
- PDF compilation errors

All errors are logged using Python's logging module.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the examples in `test_invoice.py`
2. Review the template syntax documentation
3. Ensure all dependencies are installed
4. Verify LaTeX installation for PDF compilation

## Advanced Usage

### Custom Filters

You can add custom filters to the Jinja2 environment:

```python
def custom_filter(value):
    return value.upper()

generator.env.filters['upper'] = custom_filter
```

### Multiple Templates

Generate multiple documents with different templates:

```python
templates = ["invoice.tex", "receipt.tex", "report.tex"]
for template in templates:
    generator.generate_latex(template, data, f"output/{template}")
```

### Batch Processing

Process multiple JSON files:

```python
import glob

json_files = glob.glob("data/*.json")
for json_file in json_files:
    output_name = json_file.replace("data/", "output/").replace(".json", ".tex")
    generator.generate_latex("template.tex", json_file, output_name)
``` 