#!/usr/bin/env python3
"""
Universal LaTeX document generator that populates LaTeX templates with JSON data using Jinja2.
Supports folder-based document organization where each document type has its own folder.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Union, Optional
from jinja2 import Environment, FileSystemLoader, Template
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LaTeXGenerator:
    """
    Universal LaTeX document generator that populates LaTeX templates with JSON data using Jinja2.
    """
    
    def __init__(self, template_dir: Union[str, Path] = "templates", components_dir: Union[str, Path] = "components"):
        """
        Initialize the LaTeX generator.
        
        Args:
            template_dir (Union[str, Path]): Directory containing LaTeX templates
            components_dir (Union[str, Path]): Directory containing LaTeX components
        """
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # Initialize components directory
        self.components_dir = Path(components_dir)
        self.components_dir.mkdir(exist_ok=True)
        
        # Load components
        self.components = self._load_components()
        
        # Create Jinja2 environment with custom delimiters to avoid conflicts with LaTeX
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            variable_start_string='\\VAR{',
            variable_end_string='}',
            block_start_string='\\BLOCK{',
            block_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}'
        )
        
        # Add custom filters
        self.env.filters['latex_escape'] = self._latex_escape
        self.env.filters['currency'] = self._format_currency
        self.env.filters['date_format'] = self._format_date
        self.env.filters['image'] = self._format_image
        
        # Add component functions
        self.env.globals['component'] = self._get_component
        self.env.globals['components'] = self.components
        
    def _load_components(self) -> Dict[str, str]:
        """
        Load all LaTeX components from the components directory.
        
        Returns:
            Dict[str, str]: Dictionary mapping component names to their LaTeX content
        """
        components = {}
        
        if not self.components_dir.exists():
            return components
            
        for component_file in self.components_dir.glob("*.tex"):
            component_name = component_file.stem
            try:
                with open(component_file, 'r', encoding='utf-8') as f:
                    components[component_name] = f.read()
                logger.info(f"Loaded component: {component_name}")
            except Exception as e:
                logger.error(f"Error loading component {component_name}: {e}")
                
        return components
    
    def _get_component(self, component_name: str, **kwargs) -> str:
        """
        Get a component and optionally render it with parameters.
        
        Args:
            component_name (str): Name of the component
            **kwargs: Parameters to substitute in the component
            
        Returns:
            str: Component LaTeX content, potentially with substitutions
        """
        if component_name not in self.components:
            logger.warning(f"Component '{component_name}' not found")
            return f"% Component '{component_name}' not found"
        
        component_content = self.components[component_name]
        
        # If parameters are provided, treat the component as a Jinja template
        if kwargs:
            try:
                template = Template(component_content, 
                                  variable_start_string='\\VAR{',
                                  variable_end_string='}',
                                  block_start_string='\\BLOCK{',
                                  block_end_string='}')
                return template.render(**kwargs)
            except Exception as e:
                logger.error(f"Error rendering component {component_name}: {e}")
                return f"% Error rendering component {component_name}: {e}"
        
        return component_content
    
    def list_components(self) -> list:
        """
        List all available components.
        
        Returns:
            list: List of component names
        """
        return list(self.components.keys())
    
    def add_component(self, component_name: str, latex_content: str, save_to_file: bool = True) -> None:
        """
        Add a new component.
        
        Args:
            component_name (str): Name of the component
            latex_content (str): LaTeX content of the component
            save_to_file (bool): Whether to save the component to a file
        """
        self.components[component_name] = latex_content
        
        if save_to_file:
            component_file = self.components_dir / f"{component_name}.tex"
            with open(component_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            logger.info(f"Saved component '{component_name}' to {component_file}")
    
    def get_component_content(self, component_name: str) -> Optional[str]:
        """
        Get the raw content of a component.
        
        Args:
            component_name (str): Name of the component
            
        Returns:
            Optional[str]: Component content or None if not found
        """
        return self.components.get(component_name)
    
    def _latex_escape(self, text: str) -> str:
        """
        Escape special LaTeX characters in text.
        
        Args:
            text (str): Text to escape
            
        Returns:
            str: Escaped text safe for LaTeX
        """
        if not isinstance(text, str):
            text = str(text)
            
        # LaTeX special characters that need escaping
        # Note: Order matters - escape backslash first to avoid double-escaping
        latex_special_chars = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('^', r'\textasciicircum{}'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
        ]
        
        for char, replacement in latex_special_chars:
            text = text.replace(char, replacement)
            
        return text
    
    def _format_currency(self, amount: Union[int, float], currency: str = "\\$") -> str:
        """
        Format a number as currency.
        
        Args:
            amount (Union[int, float]): Amount to format
            currency (str): Currency symbol (LaTeX-escaped)
            
        Returns:
            str: Formatted currency string
        """
        return f"{currency}{amount:,.2f}"
    
    def _format_date(self, date_str: str, format_str: str = "%B %d, %Y") -> str:
        """
        Format a date string.
        
        Args:
            date_str (str): Date string to format
            format_str (str): Target format string
            
        Returns:
            str: Formatted date string
        """
        try:
            if isinstance(date_str, str):
                # Try common date formats
                for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        return date_obj.strftime(format_str)
                    except ValueError:
                        continue
            return date_str
        except Exception:
            return date_str
    
    def _format_image(self, image_path: str, *args, **kwargs) -> str:
        """
        Format an image path for LaTeX includegraphics.
        
        Args:
            image_path (str): Path to the image file
            *args: Positional arguments for image options (e.g., "width=2in", "height=3cm")
            **kwargs: Keyword arguments for image options
            
        Returns:
            str: LaTeX includegraphics command
        """
        if not isinstance(image_path, str):
            image_path = str(image_path)
        
        # Escape path for LaTeX (handle backslashes for Windows paths)
        escaped_path = image_path.replace('\\', '/')
        
        # Build options list from positional arguments
        options = []
        for arg in args:
            if isinstance(arg, str):
                options.append(arg)
        
        # Build options from keyword arguments
        for key, value in kwargs.items():
            if value is not None:
                options.append(f"{key}={value}")
        
        # Build the includegraphics command
        if options:
            options_str = ",".join(options)
            return f"\\includegraphics[{options_str}]{{{escaped_path}}}"
        else:
            return f"\\includegraphics{{{escaped_path}}}"
    
    def load_json_data(self, json_file: Union[str, Path]) -> Dict[str, Any]:
        """
        Load JSON data from a file.
        
        Args:
            json_file (Union[str, Path]): Path to JSON file
            
        Returns:
            Dict[str, Any]: Loaded JSON data
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Successfully loaded JSON data from {json_file}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON file {json_file}: {e}")
            raise
    
    def generate_latex(self, 
                      template_name: str, 
                      data: Union[Dict[str, Any], str, Path], 
                      output_file: Union[str, Path] = None) -> str:
        """
        Generate LaTeX document from template and data.
        
        Args:
            template_name (str): Name of the LaTeX template file
            data (Union[Dict[str, Any], str, Path]): JSON data or path to JSON file
            output_file (Union[str, Path], optional): Output file path
            
        Returns:
            str: Generated LaTeX content
        """
        try:
            # Load data if it's a file path
            if isinstance(data, (str, Path)):
                data = self.load_json_data(data)
            
            # Load and render template
            template = self.env.get_template(template_name)
            latex_content = template.render(**data)
            
            # Save to file if output_file is specified
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                logger.info(f"LaTeX document saved to {output_path}")
            
            return latex_content
            
        except Exception as e:
            logger.error(f"Error generating LaTeX document: {e}")
            raise
    
    def generate_from_string_template(self, 
                                    template_content: str, 
                                    data: Union[Dict[str, Any], str, Path], 
                                    output_file: Union[str, Path] = None) -> str:
        """
        Generate LaTeX document from template string and data.
        
        Args:
            template_content (str): LaTeX template content as string
            data (Union[Dict[str, Any], str, Path]): JSON data or path to JSON file
            output_file (Union[str, Path], optional): Output file path
            
        Returns:
            str: Generated LaTeX content
        """
        try:
            # Load data if it's a file path
            if isinstance(data, (str, Path)):
                data = self.load_json_data(data)
            
            # Create template from string
            template = self.env.from_string(template_content)
            latex_content = template.render(**data)
            
            # Save to file if output_file is specified
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                logger.info(f"LaTeX document saved to {output_path}")
            
            return latex_content
            
        except Exception as e:
            logger.error(f"Error generating LaTeX document from string template: {e}")
            raise
    
    def compile_latex_to_pdf(self, latex_file: Union[str, Path], output_dir: Union[str, Path] = None) -> bool:
        """
        Compile LaTeX file to PDF using Tectonic.
        
        Args:
            latex_file (Union[str, Path]): Path to LaTeX file
            output_dir (Union[str, Path], optional): Output directory for PDF
            
        Returns:
            bool: True if compilation successful, False otherwise
        """
        try:
            import subprocess
            import shutil
            
            latex_path = Path(latex_file)
            if not latex_path.exists():
                logger.error(f"LaTeX file {latex_path} does not exist")
                return False
            
            # Check if Tectonic is available
            if not shutil.which("tectonic"):
                logger.error("Tectonic not found. Install with: brew install tectonic")
                return False
            
            # Set working directory and output directory
            work_dir = latex_path.parent
            if output_dir:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
            else:
                output_path = work_dir
            
            # Build Tectonic command with absolute path
            cmd = ["tectonic", str(latex_path.resolve())]
            
            # Determine if we need to move the PDF after compilation
            move_pdf = output_dir and output_path != work_dir
            
            # Run Tectonic compilation
            logger.info(f"Compiling with Tectonic: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
            
            if result.returncode == 0:
                logger.info(f"Successfully compiled {latex_file} to PDF using Tectonic")
                
                # Move PDF if needed (Tectonic outputs to same directory as .tex file by default)
                if move_pdf:
                    pdf_name = latex_path.stem + ".pdf"
                    src_pdf = work_dir / pdf_name
                    dst_pdf = output_path / pdf_name
                    if src_pdf.exists():
                        shutil.move(str(src_pdf), str(dst_pdf))
                        logger.info(f"Moved PDF to {dst_pdf}")
                
                return True
            else:
                logger.error(f"Error compiling LaTeX with Tectonic:")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error compiling LaTeX to PDF: {e}")
            return False

    def generate_pdf(self, 
                    template_name: str, 
                    data: Union[Dict[str, Any], str, Path], 
                    output_filename: str = None,
                    output_dir: Union[str, Path] = "output") -> str:
        """
        Generate LaTeX document and compile to PDF.
        
        Args:
            template_name (str): Name of the LaTeX template file
            data (Union[Dict[str, Any], str, Path]): JSON data or path to JSON file
            output_filename (str, optional): Output filename (without extension)
            output_dir (Union[str, Path]): Output directory for files
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            # Generate output filename if not provided
            if not output_filename:
                output_filename = Path(template_name).stem + "_output"
            
            # Ensure output directory exists
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate LaTeX file
            latex_filename = output_filename + ".tex"
            latex_filepath = output_path / latex_filename
            
            latex_content = self.generate_latex(template_name, data, latex_filepath)
            
            # Compile to PDF
            pdf_success = self.compile_latex_to_pdf(latex_filepath, output_path)
            
            if pdf_success:
                pdf_filepath = output_path / (output_filename + ".pdf")
                return str(pdf_filepath)
            else:
                raise Exception("PDF compilation failed")
                
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def generate_document_from_folder(self, 
                                    json_file: Union[str, Path], 
                                    template_name: str = None,
                                    output_dir: Union[str, Path] = None) -> str:
        """
        Generate PDF document from a folder-based structure.
        
        Args:
            json_file (Union[str, Path]): Path to JSON data file
            template_name (str, optional): Template file name (defaults to template.tex)
            output_dir (Union[str, Path], optional): Output directory (defaults to same as JSON file)
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            json_path = Path(json_file)
            if not json_path.exists():
                raise FileNotFoundError(f"JSON file not found: {json_path}")
            
            # Get the folder containing the JSON file
            document_folder = json_path.parent
            
            # Default template name
            if template_name is None:
                template_name = "template.tex"
            
            # Look for template in the same folder as JSON file
            template_path = document_folder / template_name
            if not template_path.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")
            
            # Set output directory (same as JSON file by default)
            if output_dir is None:
                output_dir = document_folder
            else:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
            
            # Load JSON data
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Create a temporary environment for this document folder
            temp_env = Environment(
                loader=FileSystemLoader(document_folder),
                variable_start_string='\\VAR{',
                variable_end_string='}',
                block_start_string='\\BLOCK{',
                block_end_string='}',
                comment_start_string='\\#{',
                comment_end_string='}'
            )
            
            # Add all the same filters and globals
            temp_env.filters['latex_escape'] = self._latex_escape
            temp_env.filters['currency'] = self._format_currency
            temp_env.filters['date_format'] = self._format_date
            temp_env.filters['image'] = self._format_image
            temp_env.globals['component'] = self._get_component
            temp_env.globals['components'] = self.components
            
            # Load and render template
            template = temp_env.get_template(template_name)
            latex_content = template.render(**data)
            
            # Generate output filename
            output_filename = json_path.stem
            latex_file = output_dir / f"{output_filename}.tex"
            
            # Save LaTeX file
            with open(latex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            logger.info(f"Generated LaTeX file: {latex_file}")
            
            # Compile to PDF
            pdf_success = self.compile_latex_to_pdf(latex_file, output_dir)
            
            if pdf_success:
                pdf_file = output_dir / f"{output_filename}.pdf"
                logger.info(f"Generated PDF file: {pdf_file}")
                return str(pdf_file)
            else:
                raise Exception("PDF compilation failed")
                
        except Exception as e:
            logger.error(f"Error generating document from folder: {e}")
            raise

# Convenience function for quick usage
def generate_latex_document(template_file: str, 
                          data_file: str, 
                          output_file: str = None,
                          template_dir: str = "templates") -> str:
    """
    Convenience function to generate LaTeX document.
    
    Args:
        template_file (str): LaTeX template file name
        data_file (str): JSON data file path
        output_file (str, optional): Output LaTeX file path
        template_dir (str): Template directory path
        
    Returns:
        str: Generated LaTeX content
    """
    generator = LaTeXGenerator(template_dir)
    return generator.generate_latex(template_file, data_file, output_file)

def main():
    """
    Command-line interface for the LaTeX generator.
    """
    parser = argparse.ArgumentParser(
        description="Universal LaTeX document generator with folder-based organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate PDF from JSON file (looks for template.tex in same folder)
  python latex_generator.py data.json
  
  # Generate PDF with custom template name
  python latex_generator.py data.json -t invoice_template.tex
  
  # Generate PDF with custom output directory
  python latex_generator.py data.json -o ./output/
  
  # List available components
  python latex_generator.py --list-components
  
Folder Structure:
  invoices/
    ├── data.json          # Your data file
    ├── template.tex       # LaTeX template (or custom name)
    └── resources/         # Images, etc.
        """
    )
    
    # Main arguments
    parser.add_argument('json_file', nargs='?', help='JSON data file path')
    parser.add_argument('-t', '--template', default='template.tex', 
                       help='Template file name (default: template.tex)')
    parser.add_argument('-o', '--output', help='Output directory (default: same as JSON file)')
    parser.add_argument('-c', '--components', default='components', 
                       help='Components directory (default: components)')
    
    # Options
    parser.add_argument('--list-components', action='store_true',
                       help='List available components and exit')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress all output except errors')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    
    try:
        # Get the script directory to find components
        script_dir = Path(__file__).parent
        components_dir = script_dir / args.components
        
        # Initialize generator
        generator = LaTeXGenerator(components_dir=components_dir)
        
        # Handle list components
        if args.list_components:
            print("Available components:")
            for component in generator.list_components():
                print(f"  - {component}")
            return
        
        # Validate JSON file argument
        if not args.json_file:
            parser.error("JSON file is required (use --list-components to list components)")
        
        # Generate document
        pdf_path = generator.generate_document_from_folder(
            json_file=args.json_file,
            template_name=args.template,
            output_dir=args.output
        )
        
        print(f"✅ Successfully generated: {pdf_path}")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 