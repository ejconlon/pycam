#!/usr/bin/env python3
"""
Script to remove GtkAction objects from UI files completely
"""

import os
import re
import glob

def remove_gtkactions(filepath):
    """Remove all GtkAction objects from a UI file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove complete GtkAction objects (multi-line)
    # This regex matches from <object class="GtkAction" to its closing </object>
    gtkaction_pattern = r'  <object class="GtkAction"[^>]*>.*?</object>\n'
    content = re.sub(gtkaction_pattern, '', content, flags=re.DOTALL)
    
    if content != original_content:
        # Create backup if not exists
        backup_path = filepath + '.pre-gtkaction-removal'
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  Created backup: {backup_path}")
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Removed GtkAction objects from: {filepath}")
        return True
    else:
        print(f"  No GtkAction objects found: {filepath}")
        return False

def main():
    """Remove GtkAction objects from all UI files"""
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    
    if not os.path.exists(ui_dir):
        print(f"UI directory not found: {ui_dir}")
        return
    
    # Find all .ui files that might contain GtkAction
    ui_files = glob.glob(os.path.join(ui_dir, "*.ui"))
    
    # Skip backup files and minimal files
    ui_files = [f for f in ui_files if not any(x in f for x in ['.backup', '.pre-', 'minimal'])]
    
    print(f"Found {len(ui_files)} UI files to process")
    
    updated_count = 0
    for ui_file in sorted(ui_files):
        if remove_gtkactions(ui_file):
            updated_count += 1
    
    print(f"\nSummary: Removed GtkActions from {updated_count} out of {len(ui_files)} files")

if __name__ == "__main__":
    main()