#!/usr/bin/env python3

import re
import glob

def fix_final_gtk4_issues(content):
    """Fix remaining GTK 4 compatibility issues"""
    
    # Remove more deprecated properties
    deprecated_props = [
        'draw_indicator', 'window_position', 'can_default', 
        'has_focus', 'update_policy', 'width_chars', 'truncate_multiline',
        'single_line_mode', 'xpad', 'ypad', 'pattern'
    ]
    
    for prop in deprecated_props:
        pattern = rf'[ \t]*<property name="{prop}">.*?</property>\n'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Fix internal-child issues for dialogs
    content = re.sub(r'<child internal-child="vbox">', '<child>', content)
    content = re.sub(r'<child internal-child="action_area">', '<child>', content)
    
    return content

def process_ui_files():
    ui_files = glob.glob('share/ui/*.ui')
    
    for file_path in ui_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_final_gtk4_issues(content)
        
        if content != original_content:
            print(f"Fixing final GTK 4 issues in {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    process_ui_files()
    print("Done fixing final GTK 4 issues")