"""
Script to translate French documentation to English using deep-translator
"""
import os
import re
from pathlib import Path
from deep_translator import GoogleTranslator

def should_translate(line):
    """Check if a line should be translated (exclude code blocks, directives, etc.)"""
    # Don't translate empty lines
    if not line.strip():
        return False
    
    # Don't translate restructuredtext directives
    if line.strip().startswith('..'):
        return False
    
    # Don't translate lines starting with special characters
    if line.strip().startswith((':','*','-','#','=')):
        return False
    
    # Don't translate lines that look like code or paths
    if '```' in line or '.. code-block::' in line:
        return False
    
    return True

def translate_rst_file(file_path):
    """Translate a restructuredtext file from French to English"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translator = GoogleTranslator(source='fr', target='en')
    translated_lines = []
    in_code_block = False
    in_math_block = False
    
    for line in lines:
        # Check if we're in a code block
        if '.. code-block::' in line or '```' in line:
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue
        
        # Check if we're in a math block
        if '.. math::' in line:
            in_math_block = True
            translated_lines.append(line)
            continue
        
        # Skip math block content
        if in_math_block and line.strip() and not line.strip().startswith('..'):
            if line.startswith('  '):  # Still in math block
                translated_lines.append(line)
                continue
            else:
                in_math_block = False
        
        # Don't translate code blocks or math
        if in_code_block or in_math_block:
            translated_lines.append(line)
            continue
        
        # Try to translate the line
        if should_translate(line):
            try:
                # Only translate if the line contains French words
                if any(word in line.lower() for word in ['le ', 'la ', 'les ', 'des ', 'du ', 'de ', 'à ', 'et ', 'pour ', 'sur ']):
                    translated = translator.translate(line.strip())
                    # Preserve indentation
                    indent = len(line) - len(line.lstrip())
                    translated_lines.append(' ' * indent + translated + '\n')
                else:
                    translated_lines.append(line)
            except Exception as e:
                print(f"  Warning: Could not translate line: {e}")
                translated_lines.append(line)
        else:
            translated_lines.append(line)
    
    # Write the translated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
    
    print(f"  ✓ Translated: {file_path}")

def main():
    """Main function to translate all RST files"""
    docs_path = Path(r'a:\OneDrive\_Github_\EnergySystemModels-en\docs\source')
    
    # Find all .rst files
    rst_files = list(docs_path.rglob('*.rst'))
    
    print(f"Found {len(rst_files)} RST files to process")
    
    for rst_file in rst_files:
        try:
            translate_rst_file(rst_file)
        except Exception as e:
            print(f"  ✗ Error processing {rst_file}: {e}")
    
    print("\nTranslation complete!")

if __name__ == '__main__':
    main()
