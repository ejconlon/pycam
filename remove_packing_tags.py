#!/usr/bin/env python3

import re
import os
import glob

def remove_packing_tags(content):
    """Remove all <packing>...</packing> blocks from UI content"""
    # Pattern to match entire <packing> blocks including nested content
    pattern = r'[ \t]*<packing>.*?</packing>\n'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def process_ui_files():
    ui_files = glob.glob('share/ui/*.ui')
    
    for file_path in ui_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = remove_packing_tags(content)
        
        if content != original_content:
            print(f"Removing packing tags from {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"No packing tags in {file_path}")

if __name__ == '__main__':
    process_ui_files()
    print("Done removing packing tags")