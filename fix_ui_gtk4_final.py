#!/usr/bin/env python3
"""
Final script to fix the remaining specific GTK 4 compatibility issues in UI files
"""

import os
import re
import glob

def fix_ui_file_final(filepath):
    """Fix final GTK 4 compatibility issues in a single UI file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove type_hint property from GtkDialog (deprecated in GTK 4)
    content = re.sub(r'    <property name="type_hint">.*?</property>\n', '', content)
    
    # Fix 2: Replace GtkButtonBox with GtkBox (GtkButtonBox deprecated)
    content = re.sub(r'<object class="GtkButtonBox"', '<object class="GtkBox"', content)
    # Ensure orientation property exists for converted ButtonBox
    buttonbox_pattern = r'(<object class="GtkBox"[^>]*>)(?!\s*<property name="orientation">)'
    content = re.sub(buttonbox_pattern, r'\1\n      <property name="orientation">horizontal</property>', content)
    
    # Fix 3: Remove layout_style property (not supported in GTK 4)
    content = re.sub(r'    <property name="layout_style">.*?</property>\n', '', content)
    
    # Fix 4: Remove all packing tags and their contents (GTK 4 uses different layout system)
    packing_pattern = r'    <packing>.*?</packing>\n'
    content = re.sub(packing_pattern, '', content, flags=re.DOTALL)
    
    # Fix 5: Fix broken XML structure - unclosed child elements
    # Remove orphaned closing child tags that don't match any opening
    content = re.sub(r'^\s*</child>\s*$', '', content, flags=re.MULTILINE)
    
    # Fix 6: Fix nested orientation properties (remove duplicates)
    # Look for double orientation properties and remove duplicates
    double_orientation = r'(<property name="orientation">[^<]*</property>\s*<property name="visible">[^<]*</property>\s*<property name="can_focus">[^<]*</property>\s*)<property name="orientation">[^<]*</property>\s*'
    content = re.sub(double_orientation, r'\1', content)
    
    # Fix 7: Remove GtkToggleAction objects (not supported in GTK 4)
    toggle_action_pattern = r'  <object class="GtkToggleAction"[^>]*>.*?</object>\n'
    content = re.sub(toggle_action_pattern, '', content, flags=re.DOTALL)
    
    # Fix 8: Clean up malformed child tags
    # Remove empty child sections
    content = re.sub(r'    <child>\s*</child>\n', '', content)
    content = re.sub(r'        <child>\s*</child>\n', '', content)
    content = re.sub(r'          <child>\s*</child>\n', '', content)
    
    # Fix 9: Remove stock labels (use plain text instead)
    stock_labels = {
        'gtk-delete': 'Delete',
        'gtk-clear': 'Clear', 
        'gtk-apply': 'Apply',
        'gtk-select-all': 'Select All',
        'gtk-go-up': '↑',
        'gtk-go-down': '↓'
    }
    for stock, replacement in stock_labels.items():
        content = re.sub(f'<property name="label">{stock}</property>', 
                        f'<property name="label">{replacement}</property>', content)
    
    # Fix 10: Clean up broken XML structure in opengl.ui specifically
    if 'opengl.ui' in filepath:
        # Fix broken child closing tags
        content = re.sub(r'^\s*</child>\s*$\n^\s*</object>$', '      </object>', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*</child>$\n(?=\s*<child)', '', content, flags=re.MULTILINE)
    
    # If content changed, write it back
    if content != original_content:
        # Create backup
        backup_path = filepath + '.final-backup'
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
    """Fix remaining UI compatibility issues"""
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
        if fix_ui_file_final(ui_file):
            updated_count += 1
    
    print(f"\nSummary: Updated {updated_count} out of {len(ui_files)} files")

if __name__ == "__main__":
    main()