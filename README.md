# Cheatsheet Generator

This application generates HTML cheatsheets from YAML templates.

## Features

- Convert YAML templates to HTML cheatsheets
- Customizable styling
- Easy-to-use command-line interface

## Requirements

- Python 3.6+
- PyYAML
- Jinja2

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cheatsheet-generator.git
   cd cheatsheet-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Create a YAML template file (e.g., `my_cheatsheet.yaml`) using the provided `template.yaml` as a guide. The YAML file should have the following structure:

   ```yaml
   title: "Your Cheatsheet Title"
   description: "A brief description of your cheatsheet"
   sections:
     - name: "Section Name"
       items:
         - title: "Item Title"
           description: "Item Description"
           code: "Example code"
   ```

2. Run the generator script:
   ```
   python generate_cheatsheet.py my_cheatsheet.yaml
   ```

3. The generated HTML cheatsheet will be saved in the same directory as the input YAML file, with the name format: `your_cheatsheet_title_cheatsheet.html`.

## Customization

You can customize the appearance of your cheatsheets by modifying the HTML template in `cheatsheet_template.html`. The template uses Jinja2 for rendering, so you can adjust the HTML structure and CSS styles as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.