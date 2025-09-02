#!/usr/bin/env python3

import re
import glob

def remove_relief_properties(content):
    """Remove relief properties which are deprecated in GTK 4"""
    return re.sub(r'[ \t]*<property name="relief">.*?</property>\n', '', content)

def process_ui_files():
    ui_files = glob.glob('share/ui/*.ui')
    
    for file_path in ui_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = remove_relief_properties(content)
        
        if content != original_content:
            print(f"Removing relief properties from {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    process_ui_files()
    print("Done removing relief properties")