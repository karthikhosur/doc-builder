# 📄 How to Add Your Own New Documents

This guide shows you how to create your own document types in the LaTeX Generator project. I'll walk you through the complete process using a "Contract" document as an example.

## 🎯 Overview

Each document type in this project follows a simple structure:
```
your-document-type/
├── template.tex          # LaTeX template with Jinja2 variables
├── data.json            # Sample data in JSON format
└── resources/           # Images, logos, etc. (optional)
```

## 📋 Step-by-Step Guide

### Step 1: Create Your Document Directory

```bash
mkdir -p your-document-type
mkdir -p your-document-type/resources
```

### Step 2: Create Your LaTeX Template

Create `your-document-type/template.tex` with your document structure:

```latex
\documentclass[a4paper,11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[a4paper,top=1cm,bottom=2cm,left=1.5cm,right=1.5cm]{geometry}
\usepackage{fontspec}
\setmainfont{Arial}
\usepackage{booktabs}
\usepackage{tcolorbox}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{adjustbox}
\usepackage{array}
\usepackage{tikz}
\usepackage{lastpage}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{colortbl}

\begin{document}

% Setup footer on all pages
\VAR{component('setup_footer', 
    company_name=company.name,
    footer_text=company.footer_text
)}

% Your document content here
\VAR{your_variable_name}

% Use components for reusable elements
\VAR{component('header_company', 
    company_name=company.name,
    address=company.address,
    phone=company.phone,
    email=company.email
)}

\end{document}
```

### Step 3: Create Your JSON Data File

Create `your-document-type/data.json` with your sample data:

```json
{
  "company": {
    "name": "Your Company Name",
    "address": "123 Business Street\\\\City, State 12345",
    "phone": "(555) 123-4567",
    "email": "contact@yourcompany.com",
    "footer_text": "Your footer text here"
  },
  "your_section": {
    "title": "Your Document Title",
    "content": "Your content here"
  }
}
```

### Step 4: Test Your Document

```bash
# Activate virtual environment
source venv/bin/activate

# Generate your document
python latex_generator.py your-document-type/data.json
```

## 🔧 Available Components

The project comes with many reusable components. Use them in your templates:

### Header Components
- `header_company` - Basic company header
- `header_company_logo` - Company header with logo

### Table Components
- `table_basic` - Simple table
- `table_professional` - Professional styled table

### List Components
- `bullet_list` - Bullet point list
- `numbered_list` - Numbered list

### Other Components
- `contact_info` - Contact information block
- `signature` - Signature block
- `section_box` - Styled content box
- `quote` - Quote block
- `footer_company` - Company footer

### Usage Example:
```latex
\VAR{component('table_professional', 
    headers=['Column 1', 'Column 2', 'Column 3'],
    rows=your_data_table,
    title='Your Table Title'
)}
```

## 📝 Jinja2 Template Syntax

### Variables
```latex
\VAR{variable_name}
\VAR{object.property}
\VAR{object.property | filter}
```

### Conditionals
```latex
\BLOCK{if condition}
    Content to show if condition is true
\BLOCK{endif}

\BLOCK{if object.property}
    Content if property exists
\BLOCK{else}
    Alternative content
\BLOCK{endif}
```

### Loops
```latex
\BLOCK{for item in items}
    \VAR{item.name} - \VAR{item.value}
\BLOCK{endfor}
```

## 🎨 Available Filters

### Currency Filter
```latex
\VAR{amount | currency}          # $1,234.56
\VAR{amount | currency("€")}     # €1,234.56
```

### Date Filter
```latex
\VAR{date | date_format}                    # January 15, 2024
\VAR{date | date_format("%Y-%m-%d")}       # 2024-01-15
```

### Image Filter
```latex
\VAR{image_path | image}                    # Basic image
\VAR{image_path | image("width=2in")}      # Image with width
\VAR{image_path | image("scale=0.8")}      # Scaled image
```

### LaTeX Escape Filter
```latex
\VAR{user_input | latex_escape}            # Escapes LaTeX special characters
```

## 📊 Example: Complete Contract Document

Here's a complete example of the contract document we created:

### Template Structure
```latex
\documentclass[a4paper,11pt]{article}
% ... packages ...

\begin{document}

% Header and footer
\VAR{component('setup_footer', company_name=company.name, footer_text=company.footer_text)}
\VAR{component('header_company_logo', company_name=company.name, ...)}

% Document title
\begin{center}
    {\LARGE \textbf{SERVICE AGREEMENT}}
\end{center}

% Contract details
\begin{tabular}{ll}
    \textbf{Contract Number:} & \VAR{contract.number} \\
    \textbf{Effective Date:} & \VAR{contract.effective_date} \\
\end{tabular}

% Service breakdown table
\VAR{component('table_professional', 
    headers=['Service Item', 'Description', 'Quantity', 'Rate', 'Total'],
    rows=contract.service_items,
    title='Service Breakdown'
)}

% Terms and conditions
\VAR{component('numbered_list', items=contract.terms_and_conditions)}

% Signatures
% ... signature sections ...

\end{document}
```

### Data Structure
```json
{
  "company": {
    "name": "TechCorp Solutions Inc.",
    "address": "123 Business Avenue\\\\Suite 200\\\\Tech City, TC 12345",
    "phone": "(555) 123-4567",
    "email": "legal@techcorp.com",
    "website": "www.techcorp.com",
    "logo_path": "",
    "footer_text": "This contract is confidential and legally binding.",
    "authorized_signatory": "Sarah Johnson",
    "signatory_title": "Chief Executive Officer"
  },
  "client": {
    "name": "Innovation Enterprises LLC",
    "contact_person": "Michael Chen",
    "address": "456 Innovation Drive\\\\Business Park\\\\Innovation City, IC 67890",
    "email": "michael.chen@innovationenterprises.com",
    "phone": "(555) 987-6543",
    "authorized_signatory": "Michael Chen",
    "signatory_title": "Chief Technology Officer"
  },
  "contract": {
    "number": "CON-2024-001",
    "date": "January 15, 2024",
    "effective_date": "February 1, 2024",
    "expiry_date": "January 31, 2025",
    "services_description": "Comprehensive software development services...",
    "service_items": [
      ["Web Development", "Custom e-commerce platform", "1", "15000.00", "15000.00"],
      ["Database Design", "MySQL architecture", "1", "5000.00", "5000.00"]
    ],
    "total_value": 74000.00,
    "payment_schedule": "50% upfront, 25% at midpoint, 25% upon completion",
    "payment_method": "Bank transfer or certified check",
    "terms_and_conditions": [
      "All work will be completed according to timeline",
      "Intellectual property transfers upon final payment",
      "Confidentiality maintained throughout contract"
    ],
    "special_clauses": [
      "Force majeure clause for unforeseen circumstances",
      "Non-compete agreement for 12 months"
    ]
  }
}
```

## 🚀 Running Your New Document

```bash
# Generate the document
python latex_generator.py your-document-type/data.json

# With custom output
python latex_generator.py your-document-type/data.json -o my_document.pdf

# With custom template
python latex_generator.py your-document-type/data.json -t my_custom_template.tex
```

## 💡 Tips and Best Practices

### 1. **Data Structure**
- Use nested objects for organization
- Keep data types consistent
- Use arrays for lists and tables

### 2. **LaTeX Safety**
- Avoid special LaTeX characters in data (`&`, `%`, `$`, `#`, `^`, `_`, `{`, `}`)
- Use `latex_escape` filter for user input
- Escape backslashes in addresses: `\\\\`

### 3. **Component Usage**
- Reuse existing components when possible
- Keep templates modular
- Use conditional blocks for optional content

### 4. **Testing**
- Test with minimal data first
- Check LaTeX compilation errors
- Verify PDF output quality

### 5. **Images**
- Place images in `resources/` folder
- Use relative paths in data
- Support PNG, JPG, PDF formats

## 🔍 Troubleshooting

### Common Issues:

1. **LaTeX Compilation Errors**
   - Check for special characters in data
   - Verify all variables are defined
   - Ensure proper LaTeX syntax

2. **Missing Variables**
   - Use conditional blocks: `\BLOCK{if variable}...\BLOCK{endif}`
   - Provide default values in template

3. **Image Not Found**
   - Check file paths in data
   - Ensure images exist in resources folder
   - Use empty string `""` for no image

4. **Component Errors**
   - Verify component names exist
   - Check component parameter requirements
   - Use `--list-components` to see available components

## 📚 Advanced Features

### Custom Filters
You can add custom filters to the Jinja2 environment:

```python
def custom_filter(value):
    return value.upper()

generator.env.filters['upper'] = custom_filter
```

### Batch Processing
Generate multiple documents:

```python
import glob

json_files = glob.glob("your-document-type/*.json")
for json_file in json_files:
    generator.generate_latex("template.tex", json_file, f"output/{json_file}")
```

### String Templates
Use templates as strings instead of files:

```python
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
    data=your_data
)
```

## 🎉 Success!

You've now learned how to create your own document types! The key is to:

1. **Structure your data** logically in JSON
2. **Use existing components** for common elements
3. **Follow LaTeX best practices** for special characters
4. **Test incrementally** to catch errors early

Your new document type will work seamlessly with the existing LaTeX generator and can be used for mass generation just like the built-in examples!
