#!/usr/bin/env python3
"""
Script to fix remaining XML structure issues and GTK 4 dialog compatibility
"""

import os
import re
import glob

def fix_ui_structure(filepath):
    """Fix XML structure and GTK 4 dialog compatibility issues"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove broken empty child/object structures
    # Pattern: <child>\n\n      </object> or similar broken structures
    broken_child_object = r'    <child>\s*\n\s*</object>'
    content = re.sub(broken_child_object, '', content)
    
    # Fix 2: Remove orphaned closing tags
    content = re.sub(r'^\s*</object>\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*</child>\s*$', '', content, flags=re.MULTILINE)
    
    # Fix 3: Fix GTK 4 dialog structure - remove internal-child="vbox"
    # GTK 4 dialogs don't use internal vbox child
    content = re.sub(r'    <child internal-child="vbox">', '    <child>', content)
    content = re.sub(r'    <child internal-child="action_area">', '    <child>', content)
    
    # Fix 4: Clean up multiple consecutive newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Fix 5: Fix specific broken structures in opengl.ui
    if 'opengl.ui' in filepath:
        # Fix the broken child/object structure around line 9-11
        broken_frame_child = r'(<object class="GtkFrame"[^>]*>\s*<property[^>]*>[^<]*</property>\s*<property[^>]*>[^<]*</property>\s*<property[^>]*>[^<]*</property>\s*)<child>\s*</object>'
        content = re.sub(broken_frame_child, r'\1<child>\n        <placeholder/>\n      </child>', content, flags=re.DOTALL)
        
        # Remove duplicate closing objects
        content = re.sub(r'      </object>\s*</object>', '      </object>', content)
    
    # Fix 6: Fix specific broken structures in models.ui and toolpaths.ui
    if 'models.ui' in filepath or 'toolpaths.ui' in filepath:
        # Fix misplaced child tags in tree views
        misplaced_child = r'(<child internal-child="selection">\s*<object[^>]*>\s*</object>\s*)</child>\s*<child>'
        content = re.sub(misplaced_child, r'\1</child>\n                <child>', content)
    
    # Fix 7: Ensure proper XML structure for TreeView columns
    # Fix missing </child> tags before new <child> tags
    missing_child_close = r'(</object>)\s*(<child>)'
    content = re.sub(missing_child_close, r'\1\n                </child>\n                \2', content)
    
    # Fix 8: Clean up extra whitespace and ensure proper indentation
    # Remove lines with only whitespace
    content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
    
    # If content changed, write it back
    if content != original_content:
        # Create backup
        backup_path = filepath + '.structure-backup'
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  Created backup: {backup_path}")
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed structure: {filepath}")
        return True
    else:
        print(f"  No changes needed: {filepath}")
        return False

def main():
    """Fix XML structure issues in problematic UI files"""
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    
    if not os.path.exists(ui_dir):
        print(f"UI directory not found: {ui_dir}")
        return
    
    # Focus on the problematic files identified in the error log
    problem_files = [
        'opengl.ui',
        'units.ui', 
        'toolpaths.ui',
        'models.ui',
        'plugin_selector.ui',
        'processes.ui'
    ]
    
    ui_files = [os.path.join(ui_dir, filename) for filename in problem_files if os.path.exists(os.path.join(ui_dir, filename))]
    
    print(f"Found {len(ui_files)} problematic UI files to fix")
    
    updated_count = 0
    for ui_file in ui_files:
        if fix_ui_structure(ui_file):
            updated_count += 1
    
    print(f"\nSummary: Fixed structure in {updated_count} out of {len(ui_files)} files")

if __name__ == "__main__":
    main()