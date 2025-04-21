from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import json
import random

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def export_cars_to_pdf(cars, output_filename):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')

    # Get the absolute path to the template directory
    template_dir = os.path.abspath('templates')

    # Render HTML for all cars
    html_content = template.render(contents=cars)

    # Configure PDF options
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None,
        'disable-smart-shrinking': None,
        'quiet': None,
        'no-stop-slow-scripts': None,
        'javascript-delay': '1000',
        'load-error-handling': 'ignore',
        'allow': [template_dir],
        'disable-external-links': None,
        'disable-javascript': None
    }

    # Generate PDF directly from string
    try:
        pdfkit.from_string(html_content, output_filename, options=options)
        print(f"PDF generated: {output_filename}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        # Write HTML to a file for debugging
        with open('debug.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("HTML content written to debug.html for inspection")

# Example usage:
cars = read_json_file('/Users/amd/my_scrapping/autohub/autuhub_data/final_json/detail_json_mnaf_2025-02-22.json')
cars=cars[:2]
export_cars_to_pdf(cars, 'multiple_cars.pdf')