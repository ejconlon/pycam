#!/usr/bin/env python3

import re
import os
import glob

def fix_stock_properties(content):
    """Remove use_stock properties and convert stock labels to icon names"""
    
    # Stock labels to icon name mapping
    stock_to_icon = {
        'gtk-new': 'document-new',
        'gtk-delete': 'edit-delete', 
        'gtk-go-up': 'go-up',
        'gtk-go-down': 'go-down',
        'gtk-help': 'help-browser',
        'gtk-apply': 'application-exit',
        'gtk-ok': 'dialog-ok',
        'gtk-cancel': 'process-stop'
    }
    
    # Remove use_stock properties
    content = re.sub(r'[ \t]*<property name="use_stock">.*?</property>\n', '', content)
    
    # Convert stock labels to icon names
    for stock_label, icon_name in stock_to_icon.items():
        # Replace label property with icon_name property
        pattern = f'<property name="label">{re.escape(stock_label)}</property>'
        replacement = f'<property name="icon_name">{icon_name}</property>'
        content = re.sub(pattern, replacement, content)
    
    return content

def process_ui_files():
    ui_files = glob.glob('share/ui/*.ui')
    
    for file_path in ui_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_stock_properties(content)
        
        if content != original_content:
            print(f"Fixing stock properties in {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"No stock properties in {file_path}")

if __name__ == '__main__':
    process_ui_files()
    print("Done fixing stock properties")