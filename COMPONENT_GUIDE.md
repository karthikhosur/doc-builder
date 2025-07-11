# LaTeX Component System Guide

## Overview

This LaTeX generator includes a reusable component system that allows you to create and use modular LaTeX code snippets. Components are stored in the `components/` directory and can be used in any template.

## Available Components

### 1. `table_basic`
Basic table with borders.

**Usage:**
```latex
\VAR{component('table_basic', 
    headers=['Col1', 'Col2', 'Col3'],
    rows=[['A', 'B', 'C'], ['D', 'E', 'F']],
    caption='Table Caption'
)}
```

### 2. `table_professional`
Professional table with booktabs styling.

**Usage:**
```latex
\VAR{component('table_professional', 
    headers=['Item', 'Quantity', 'Price'],
    rows=[['Product A', '2', '$10.00']],
    title='Invoice Items'
)}
```

### 3. `header_company`
Company header with logo and contact info.

**Usage:**
```latex
\VAR{component('header_company', 
    company_name='My Company',
    address='123 Main St\\nCity, State 12345',
    phone='555-1234',
    email='info@company.com',
    logo_path='logo.png',
    date='2024-01-01'
)}
```

### 4. `header_company_logo`
Professional document header with logo on left and detailed company information on right.

**Usage:**
```latex
\VAR{component('header_company_logo', 
    company_name='ManpowerGroup Services India Pvt Ltd.',
    address='Metro Pillar Number 98, Vatika City Point, 6th Floor,\\\\Mehrauli-Gurgaon Rd, Sector 25,\\\\Gurugram, Haryana 122002',
    cin='U74910DL1997PTC085591',
    phone='+91 – 124 - 6795400',
    website='www.manpowergroup.com',
    logo_path='resources/logo.png',
    date='2024-01-01'
)}
```

**Features:**
- Professional 2-column table layout with precise alignment control
- Logo positioned on the left (30% width) with compact height (3.5cm)
- Company details on the right (65% width) with readable typography
- Tabular format ensures consistent top-level alignment
- Supports CIN (Corporate Identification Number)
- Website field for company URL
- Professional formatting with optimized spacing and alignment
- Includes horizontal rule separator for document structure
- Optimized for A4 paper size with minimal top padding
- Uses standard document header formatting conventions
- Responsive logo sizing with `keepaspectratio`
- Enhanced readability: normal size company name, small contact details
- Compact vertical spacing for efficient use of page space

### 5. `setup_footer`
Configures page footers that appear on all pages using the fancyhdr package.

**Usage:**
```latex
\VAR{component('setup_footer', 
    company_name='ManpowerGroup Services India Pvt Ltd.',
    footer_text='This document is confidential and intended solely for the use of the individual or entity to whom it is addressed.'
)}
```

**Features:**
- Sets up footers for all pages using fancyhdr package
- Horizontal rule separator at the top of footer
- Company name positioned on the left side
- Page numbers "Page X of Y" on the right side
- Optional centered footer text in tiny font
- Professional spacing and typography
- Requires `lastpage` package for page counting
- Requires `fancyhdr` package for page setup
- Must be called early in document (after \begin{document})

### 6. `footer_company`
Single-page footer component (deprecated - use setup_footer instead).

**Usage:**
```latex
\VAR{component('footer_company', 
    company_name='ManpowerGroup Services India Pvt Ltd.',
    footer_text='This document is confidential and intended solely for the use of the individual or entity to whom it is addressed.'
)}
```

**Note:** This component only appears on the last page. For footers on all pages, use `setup_footer` instead.

### 7. `section_box`
Colored box for highlighting content.

**Usage:**
```latex
\VAR{component('section_box', 
    title='Important Note',
    content='This is important information.',
    color='blue'
)}
```

### 8. `signature_block`
Signature block with name, title, and date.

**Usage:**
```latex
\VAR{component('signature_block', 
    name='John Doe',
    title='Manager',
    signature_image='signature.png',
    date='2024-01-01'
)}
```

### 9. `bullet_list`
Bullet point list.

**Usage:**
```latex
\VAR{component('bullet_list', 
    items=['Item 1', 'Item 2', 'Item 3']
)}
```

### 10. `numbered_list`
Numbered list.

**Usage:**
```latex
\VAR{component('numbered_list', 
    items=['First step', 'Second step', 'Third step']
)}
```

### 11. `contact_info`
Contact information block.

**Usage:**
```latex
\VAR{component('contact_info', 
    name='John Doe',
    company='ABC Corp',
    address='123 Main St',
    phone='555-1234',
    email='john@example.com'
)}
```

## How to Use Components

### In Templates

1. **Basic usage:**
   ```latex
   \VAR{component('component_name', param1='value1', param2='value2')}
   ```

2. **With complex parameters:**
   ```latex
   \VAR{component('table_basic', 
       headers=['Name', 'Age', 'City'],
       rows=[
           ['Alice', '25', 'New York'],
           ['Bob', '30', 'Los Angeles']
       ]
   )}
   ```

### In Python Code

```python
from latex_generator import LaTeXGenerator

generator = LaTeXGenerator()

# List available components
components = generator.list_components()
print(components)

# Use a component directly
table_latex = generator._get_component('table_basic',
    headers=['A', 'B'],
    rows=[['1', '2']]
)
print(table_latex)
```

## Creating New Components

### Method 1: Create a .tex file

1. Create a new file in the `components/` directory (e.g., `my_component.tex`)
2. Add your LaTeX code with Jinja2 variables:

```latex
% My Custom Component
% Usage: component('my_component', title='My Title', content='My content')

\begin{center}
    \textbf{\VAR{title}}
    \vspace{0.5cm}
    
    \VAR{content}
\end{center}
```

### Method 2: Add programmatically

```python
generator = LaTeXGenerator()

component_latex = """
% Custom Footer
\\vfill
\\begin{center}
    \\small \\VAR{text}
\\end{center}
"""

generator.add_component('my_footer', component_latex)
```

## Component Guidelines

### 1. Component Structure
- Start with a comment describing the component
- Include usage examples
- Use descriptive parameter names
- Handle optional parameters with `\BLOCK{if parameter}`

### 2. Parameter Handling
```latex
% Required parameter
\VAR{title}

% Optional parameter
\BLOCK{if subtitle}
    \VAR{subtitle}
\BLOCK{endif}

% Parameter with default
\VAR{color or 'blue'}
```

### 3. Loops and Lists
```latex
% Loop through items
\BLOCK{for item in items}
    \item \VAR{item}
\BLOCK{endfor}

% Loop with conditions
\BLOCK{for row in rows}
    \BLOCK{for cell in row}
        \VAR{cell} \BLOCK{if not loop.last}&\BLOCK{endif}
    \BLOCK{endfor} \\
\BLOCK{endfor}
```

### 4. Required Packages
If your component needs specific LaTeX packages, document them in the component file:

```latex
% Required packages: booktabs, array, xcolor
% Usage: component('my_component', ...)
```

## Example: Complete Document

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tcolorbox}

\begin{document}

\VAR{component('header_company_logo', 
    company_name='Tech Corp',
    address='123 Tech St',
    phone='555-TECH',
    website='www.techcorp.com',
    logo_path='resources/logo.png'
)}

\section{Introduction}

\VAR{component('section_box', 
    title='Welcome',
    content='This document demonstrates our component system.'
)}

\section{Features}

\VAR{component('bullet_list', 
    items=['Easy to use', 'Reusable', 'Customizable']
)}

\VAR{component('signature_block', 
    name='John Doe',
    title='CEO'
)}

\end{document}
```