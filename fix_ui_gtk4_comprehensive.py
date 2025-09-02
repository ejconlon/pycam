#!/usr/bin/env python3
"""
Comprehensive script to fix all GTK 4 compatibility issues in UI files
"""

import os
import re
import glob

def fix_ui_file_comprehensive(filepath):
    """Fix comprehensive GTK 4 compatibility issues in a single UI file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove shadow_type properties (already done)
    content = re.sub(r'    <property name="shadow_type">.*?</property>\n', '', content)
    
    # Fix 2: Remove border_width properties (already done)
    content = re.sub(r'    <property name="border_width">.*?</property>\n', '', content)
    
    # Fix 3: Update GTK version requirement (already done)
    content = re.sub(r'<requires lib="gtk\+" version="[^"]*"/>', '<requires lib="gtk" version="4.0"/>', content)
    
    # Fix 4: Remove pixbuf properties (already done)
    content = re.sub(r'    <property name="pixbuf">.*?</property>\n', '', content)
    
    # Fix 5: Remove stock_id properties (already done)
    content = re.sub(r'    <property name="stock_id">.*?</property>\n', '', content)
    
    # Fix 6: Remove use_stock properties (already done)  
    content = re.sub(r'    <property name="use_stock">.*?</property>\n', '', content)
    
    # Fix 7: Remove GtkAlignment objects (GTK 4 doesn't support GtkAlignment)
    alignment_pattern = r'  <object class="GtkAlignment"[^>]*>.*?</object>\n'
    content = re.sub(alignment_pattern, '', content, flags=re.DOTALL)
    
    # Fix 8: Remove dialog role property (deprecated in GTK 4)
    content = re.sub(r'    <property name="role">.*?</property>\n', '', content)
    
    # Fix 9: Remove stock_size property from GtkCellRendererPixbuf
    content = re.sub(r'    <property name="stock_size">.*?</property>\n', '', content)
    
    # Fix 10: Replace GtkVBox/GtkHBox with GtkBox and orientation
    content = re.sub(r'<object class="GtkVBox"', '<object class="GtkBox"', content)
    content = re.sub(r'<object class="GtkHBox"', '<object class="GtkBox"', content)
    # Add orientation property for converted boxes
    vbox_pattern = r'(<object class="GtkBox"[^>]*>)(?!\s*<property name="orientation">)'
    content = re.sub(vbox_pattern, r'\1\n      <property name="orientation">vertical</property>', content)
    
    # Fix 11: Remove deprecated packing properties and replace with modern ones
    # Replace expand and fill with hexpand/vexpand
    packing_block = r'        <packing>\s*(?:<property name="expand">[^<]*</property>\s*)?(?:<property name="fill">[^<]*</property>\s*)?(?:<property name="position">[^<]*</property>\s*)?\s*</packing>\n'
    content = re.sub(packing_block, '', content)
    
    # Fix 12: Remove window_position property (deprecated)
    content = re.sub(r'    <property name="window_position">.*?</property>\n', '', content)
    
    # Fix 13: Remove spacing from GtkButtonBox (use CSS instead in GTK 4)
    content = re.sub(r'    <property name="spacing">\d+</property>\n(?=.*GtkButtonBox)', '', content)
    
    # If content changed, write it back
    if content != original_content:
        # Create backup
        backup_path = filepath + '.comprehensive-backup'
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
    
    # Skip backup files and minimal files
    ui_files = [f for f in ui_files if not any(x in f for x in ['.backup', '.pre-', 'minimal'])]
    
    print(f"Found {len(ui_files)} UI files to process")
    
    updated_count = 0
    for ui_file in sorted(ui_files):
        if fix_ui_file_comprehensive(ui_file):
            updated_count += 1
    
    print(f"\nSummary: Updated {updated_count} out of {len(ui_files)} files")

if __name__ == "__main__":
    main()