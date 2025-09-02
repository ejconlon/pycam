#!/usr/bin/env python3
"""
Script to fix common GTK 4 compatibility issues in UI files
"""

import os
import re
import glob

def fix_ui_file(filepath):
    """Fix common GTK 4 compatibility issues in a single UI file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove shadow_type properties (not supported in GTK 4)
    content = re.sub(r'    <property name="shadow_type">.*?</property>\n', '', content)
    
    # Fix 2: Remove border_width properties from dialogs (deprecated)
    content = re.sub(r'    <property name="border_width">.*?</property>\n', '', content)
    
    # Fix 3: Update GTK version requirement
    content = re.sub(r'<requires lib="gtk\+" version="[^"]*"/>', '<requires lib="gtk" version="4.0"/>', content)
    
    # Fix 4: Remove pixbuf properties (use resource or file instead)
    content = re.sub(r'    <property name="pixbuf">.*?</property>\n', '', content)
    
    # Fix 5: Remove stock_id properties (deprecated in GTK 4)
    content = re.sub(r'    <property name="stock_id">.*?</property>\n', '', content)
    
    # Fix 6: Remove use_stock properties
    content = re.sub(r'    <property name="use_stock">.*?</property>\n', '', content)
    
    # If content changed, write it back
    if content != original_content:
        # Create backup
        backup_path = filepath + '.gtk3-backup'
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  Created backup: {backup_path}")
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filepath}")
        return True
    else:
        print(f"  No changes needed: {filepath}")
        return False

def main():
    """Fix all UI files in the share/ui directory"""
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    
    if not os.path.exists(ui_dir):
        print(f"UI directory not found: {ui_dir}")
        return
    
    # Find all .ui files
    ui_files = glob.glob(os.path.join(ui_dir, "*.ui"))
    
    # Skip backup files and our minimal file
    ui_files = [f for f in ui_files if not f.endswith('.backup') and 'minimal' not in f]
    
    print(f"Found {len(ui_files)} UI files to process")
    
    updated_count = 0
    for ui_file in sorted(ui_files):
        if fix_ui_file(ui_file):
            updated_count += 1
    
    print(f"\nSummary: Updated {updated_count} out of {len(ui_files)} files")

if __name__ == "__main__":
    main()