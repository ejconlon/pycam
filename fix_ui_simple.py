#!/usr/bin/env python3
"""
Simple script to fix missing </child> closing tags in .ui files.
Pattern: <child> followed by <object>...</object> but missing </child>
"""

import os
import re
import glob

def fix_ui_file(file_path):
    """Fix missing </child> tags in a single .ui file."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: </object> followed by empty line and then <child> or end of parent
    # This means the previous child wasn't closed
    patterns_to_fix = [
        # </object> followed by empty lines and <child>
        (r'(</object>)\n\n(\s*)<child>', r'\1\n\2</child>\n\2<child>'),
        
        # </object> followed by empty lines and </object> (end of parent)  
        (r'(</object>)\n\n(\s*)</object>', r'\1\n\2</child>\n\2</object>'),
        
        # </object> followed by empty lines and </child> (already has some closing)
        (r'(</object>)\n\n(\s*)</child>', r'\1\n\2</child>\n\2</child>'),
        
        # Special case: placeholder followed by empty lines
        (r'(<placeholder/>)\n\n(\s*)</object>', r'\1\n\2</child>\n\2</object>'),
        
        # Special case: attributes closing without child close
        (r'(</attributes>)\n\n(\s*)</object>', r'\1\n\2</child>\n\2</object>'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed {file_path}")
        return True
    else:
        print(f"  No changes needed for {file_path}")
        return False

def main():
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    
    # Get all .ui files except working files and backup files
    ui_files = glob.glob(os.path.join(ui_dir, "*.ui"))
    ui_files = [f for f in ui_files if not f.endswith('-working.ui') and not f.endswith('.backup')]
    
    fixed_count = 0
    
    for ui_file in sorted(ui_files):
        if fix_ui_file(ui_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(ui_files)} files.")

if __name__ == "__main__":
    main()