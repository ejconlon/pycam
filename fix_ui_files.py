#!/usr/bin/env python3
"""
Script to fix missing </child> closing tags in .ui files.
The issue is that many <child> tags are opened but never closed.
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
    
    # Split content into lines for easier processing
    lines = content.split('\n')
    
    # Stack to track open tags
    tag_stack = []
    fixed_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check for opening child tag
        if '<child' in line and not line.strip().endswith('/>') and not '</child>' in line:
            # This is an opening <child> tag
            indent_level = len(line) - len(line.lstrip())
            tag_stack.append(('child', indent_level, i))
            fixed_lines.append(line)
            
        # Check for opening object tag  
        elif '<object' in line and not line.strip().endswith('/>'):
            indent_level = len(line) - len(line.lstrip())
            tag_stack.append(('object', indent_level, i))
            fixed_lines.append(line)
            
        # Check for closing object tag
        elif '</object>' in line:
            # Close any child tags that should be closed before this object
            while tag_stack and tag_stack[-1][0] == 'child' and tag_stack[-1][1] >= len(line) - len(line.lstrip()):
                child_tag, child_indent, child_line = tag_stack.pop()
                # Add closing child tag with proper indentation
                closing_indent = ' ' * (child_indent + 2)  # Add 2 spaces for proper nesting
                fixed_lines.append(closing_indent + '</child>')
            
            # Remove the corresponding object from stack
            if tag_stack and tag_stack[-1][0] == 'object':
                tag_stack.pop()
                
            fixed_lines.append(line)
            
        else:
            fixed_lines.append(line)
    
    # Close any remaining child tags at the end
    while tag_stack and tag_stack[-1][0] == 'child':
        child_tag, child_indent, child_line = tag_stack.pop()
        closing_indent = ' ' * (child_indent + 2)
        fixed_lines.append(closing_indent + '</child>')
    
    new_content = '\n'.join(fixed_lines)
    
    # Only write if content changed
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
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