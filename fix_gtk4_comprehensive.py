#!/usr/bin/env python3

import re
import glob
import xml.etree.ElementTree as ET

def fix_deprecated_properties(content):
    """Fix all remaining deprecated properties and objects for GTK 4"""
    
    # Remove deprecated properties
    deprecated_props = [
        'role', 'type_hint', 'events', 'pixbuf', 'invisible_char', 
        'alpha', 'image', 'xalign', 'yalign'
    ]
    
    for prop in deprecated_props:
        pattern = rf'[ \t]*<property name="{prop}">.*?</property>\n'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Replace GtkRadioButton with GtkCheckButton (GTK 4 approach)
    content = re.sub(r'<object class="GtkRadioButton"', '<object class="GtkCheckButton"', content)
    
    # Remove group property (not needed in GTK 4 CheckButton)
    content = re.sub(r'[ \t]*<property name="group">.*?</property>\n', '', content)
    
    return content

def process_ui_files():
    ui_files = glob.glob('share/ui/*.ui')
    
    for file_path in ui_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_deprecated_properties(content)
        
        if content != original_content:
            print(f"Fixing GTK 4 compatibility issues in {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    process_ui_files()
    print("Done fixing GTK 4 compatibility issues")