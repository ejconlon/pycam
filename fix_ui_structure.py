#!/usr/bin/env python3
"""
Script to fix common GTK 4 UI file structure issues in PyCAM
"""

import os
import re
import glob
import xml.etree.ElementTree as ET

def fix_common_ui_issues(file_path):
    """Fix common UI file structure issues"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Replace unknown internal child vbox/hbox issues
    content = re.sub(r'<child internal-child="vbox">', '<child>', content)
    content = re.sub(r'<child internal-child="hbox">', '<child>', content)
    
    # Fix 2: Ensure proper child/object nesting structure
    # Find cases where <object> appears directly after a <child> without proper closing
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check for common structure issue: <child> followed by <object> at same level
        if '<child>' in line and not '<child type=' in line:
            # Look for next object at same indentation level
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # Check if we have object at wrong indentation after child
                if re.match(r'^\s*<object', next_line):
                    indent = re.match(r'^(\s*)', line).group(1)
                    next_indent = re.match(r'^(\s*)', next_line).group(1)
                    if len(next_indent) <= len(indent):
                        # This suggests missing proper nesting - but we need to be careful
                        # For now, just flag it
                        print(f"  Warning: Potential nesting issue at line {i+1}")
        
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix 3: Remove <layout> tags that aren't supported in GTK 4
    content = re.sub(r'\s*<layout>.*?</layout>\s*', '', content, flags=re.DOTALL)
    
    # Fix 4: Fix specific property name issues
    content = re.sub(r'<property name="step_incr">', '<property name="step-increment">', content)
    
    # Only write if changes were made
    if content != original_content:
        print(f"  Fixed issues in {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    else:
        print(f"  No issues found in {file_path}")
        return False

def main():
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    ui_files = glob.glob(os.path.join(ui_dir, "*.ui"))
    
    fixed_count = 0
    total_count = len(ui_files)
    
    for ui_file in sorted(ui_files):
        if fix_common_ui_issues(ui_file):
            fixed_count += 1
    
    print(f"\nSummary: Fixed {fixed_count} of {total_count} UI files")

if __name__ == "__main__":
    main()