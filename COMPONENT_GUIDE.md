# Component Library Guide

This document explains how to use the reusable LaTeX components available in the `components/` folder.

## Available Components

### 1. Generic Signature Component (`signature.tex`)
A flexible signature component that can handle text or image signatures.

**Usage:**
```
component('signature', 
    name='John Doe', 
    title='Manager', 
    signature_type='text|image', 
    signature_content='Signature text or image path', 
    date='2024-01-01', 
    position='left|right|center'
)
```

**Parameters:**
- `name`: Signatory's name
- `title`: Signatory's title/position
- `signature_type`: Either 'text' or 'image'
- `signature_content`: For text: the signature text, for image: path to signature image
- `date`: Date of signature (optional)
- `position`: Alignment - 'left', 'right', or 'center' (optional, defaults to left)

### 2. Generic Table Component (`table.tex`)
A flexible table component that can handle various configurations.

**Usage:**
```
component('table', 
    headers=['Header1', 'Header2'], 
    rows=[['Row1Col1', 'Row1Col2'], ['Row2Col1', 'Row2Col2']], 
    style='basic|professional|striped', 
    width='full|auto', 
    caption='Table Caption', 
    align='left|center|right',
    grid=true|false
)
```

**Parameters:**
- `headers`: List of table headers
- `rows`: List of lists containing table data
- `style`: Table style - 'basic', 'professional', or 'striped' (optional)
- `width`: Table width - 'full' (full page width) or 'auto' (content width) (optional)
- `caption`: Table caption (optional)
- `align`: Column alignment - 'left', 'center', or 'right' (optional, defaults to left)
- `grid`: Enable/disable all table grid lines - true or false (optional, defaults to style-based)

**Grid Parameter:**
- When `grid=true`: Shows all horizontal and vertical lines regardless of style
- When `grid=false`: Uses style-based line rendering (professional uses booktabs, basic uses simple lines)
- Full width tables (`width='full'`) automatically span the entire page width and are centered

### 3. Header with Company Logo (`header_company_logo.tex`)
Professional header with company logo and information.

**Usage:**
```
component('header_company_logo', 
    company_name='Company Name', 
    address='Address', 
    cin='CIN Number', 
    phone='Phone', 
    website='Website', 
    logo_path='logo.png', 
    date='Date'
)
```

### 4. Footer Setup (`setup_footer.tex`)
Sets up page footers with company information and page numbers.

**Usage:**
```
component('setup_footer', 
    company_name='Company Name', 
    footer_text='Optional footer text'
)
```

### 5. Section Box (`section_box.tex`)
Creates colored boxes for highlighting sections.

**Usage:**
```
component('section_box', 
    title='Section Title', 
    content='Section content', 
    color='blue|green|orange|red'
)
```

### 6. Lists (`numbered_list.tex`, `bullet_list.tex`)
Creates numbered or bulleted lists.

**Usage:**
```
component('numbered_list', items=['Item 1', 'Item 2', 'Item 3'])
component('bullet_list', items=['Item 1', 'Item 2', 'Item 3'])
```

### 7. Contact Information (`contact_info.tex`)
Formats contact information in a clean layout.

**Usage:**
```
component('contact_info', 
    name='John Doe', 
    company='Company Name', 
    address='Address', 
    phone='Phone', 
    email='Email'
)
```

## Example Usage in Templates

### Offer Letter Example
```latex
% Header
\VAR{component('header_company_logo', 
    company_name=company_name, 
    address=address, 
    cin=cin, 
    phone=phone, 
    website=website, 
    logo_path=logo_path, 
    date=date
)}

% Main content
\textbf{Date:} \VAR{date}

% Signature
\VAR{component('signature', 
    name=signatory_name, 
    title=signatory_title, 
    signature_type='text', 
    signature_content=signatory_name
)}

% Full-width table with all grids
\VAR{component('table', 
    headers=['Column 1', 'Column 2'], 
    rows=[['Data 1', 'Data 2'], ['Data 3', 'Data 4']], 
    style='basic',
    width='full',
    align='center',
    grid=true
)}
```

## Best Practices

1. **Use Generic Components**: Instead of creating specific components for each use case, use the generic `signature` and `table` components with different parameters.

2. **Escape Special Characters**: Remember to escape LaTeX special characters like `%` as `\%` in your data.

3. **Consistent Styling**: Use the same style parameters across your document for consistency.

4. **Flexible Data Structure**: Structure your JSON data to match the component parameters for easy reuse.

5. **Table Formatting**: 
   - Use `width='full'` for tables that should span the entire page
   - Use `grid=true` for tables that need complete grid lines
   - Use `align='center'` for better visual appearance in full-width tables

## Creating New Components

When creating new components:

1. Make them generic and reusable
2. Use clear parameter names
3. Include usage examples in comments
4. Handle optional parameters gracefully
5. Test with various data inputs