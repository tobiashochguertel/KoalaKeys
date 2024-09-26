import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError
import re

def validate_yaml(file_path):
    errors = []

    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
    except (ParserError, ScannerError) as e:
        return [f"YAML parsing error: {str(e)}"]

    # Check for required top-level keys
    required_keys = ['title', 'shortcuts']
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required top-level key: '{key}'")

    # Validate title
    if 'title' in data and not isinstance(data['title'], str):
        errors.append("Title must be a string")

    # Validate layout (if present)
    if 'layout' in data:
        if not isinstance(data['layout'], dict):
            errors.append("Layout must be a dictionary")
        else:
            valid_keyboards = ['US', 'UK', 'DE', 'FR', 'ES']
            valid_systems = ['Darwin', 'Linux', 'Windows']
            
            if 'keyboard' in data['layout'] and data['layout']['keyboard'] not in valid_keyboards:
                errors.append(f"Invalid keyboard layout. Must be one of: {', '.join(valid_keyboards)}")
            
            if 'system' in data['layout'] and data['layout']['system'] not in valid_systems:
                errors.append(f"Invalid system. Must be one of: {', '.join(valid_systems)}")

    # Validate shortcuts
    if 'shortcuts' in data:
        if not isinstance(data['shortcuts'], dict):
            errors.append("Shortcuts must be a dictionary")
        else:
            for category, shortcuts in data['shortcuts'].items():
                if not isinstance(shortcuts, dict):
                    errors.append(f"Category '{category}' must contain a dictionary of shortcuts")
                else:
                    for shortcut, details in shortcuts.items():
                        if not isinstance(details, dict) or 'description' not in details:
                            errors.append(f"Shortcut '{shortcut}' in category '{category}' must have a 'description' key")
                        elif not isinstance(details['description'], str):
                            errors.append(f"Description for shortcut '{shortcut}' in category '{category}' must be a string")
                        
                        # Validate shortcut format
                        if not re.match(r'^[A-Za-z0-9+⌘⌥⌃⇧←→↑↓\s\-\|\[\],.:/`"?<>=\\⌃]+$', shortcut):
                            errors.append(f"Invalid shortcut format: '{shortcut}' in category '{category}'")

    return errors

def lint_yaml(file_path):
    warnings = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines, start=1):
        # Check for lines longer than 100 characters
        if len(line.rstrip()) > 100:
            warnings.append(f"Line {i} is longer than 100 characters")

        # Check for inconsistent indentation
        indent = len(line) - len(line.lstrip())
        if indent % 2 != 0:
            warnings.append(f"Line {i} has inconsistent indentation")

        # Check for trailing whitespace
        if line.rstrip() != line.rstrip('\n'):
            warnings.append(f"Line {i} has trailing whitespace")

    return warnings

def fix_yaml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace special characters
    content = content.replace('⌘', 'cmd')
    content = content.replace('⌃', 'ctrl')
    content = content.replace('⌥', 'alt')

    # Fix indentation
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        fixed_indent = (indent // 2) * 2  # Round down to nearest even number
        fixed_lines.append(' ' * fixed_indent + stripped.rstrip())

    fixed_content = '\n'.join(fixed_lines)

    # Write fixed content back to file
    with open(file_path, 'w') as file:
        file.write(fixed_content)

def process_yaml(file_path):
    print(f"Processing {file_path}...")
    
    # Validate
    errors = validate_yaml(file_path)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Validation passed.")

    # Lint
    warnings = lint_yaml(file_path)
    if warnings:
        print("Linting warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Linting passed.")

    # Fix
    fix_yaml(file_path)
    print("YAML file has been fixed and special characters replaced.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validate_yaml.py <path_to_yaml_file>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    process_yaml(yaml_file)