#!/usr/bin/env python3
"""
Final script to fix missing </child> closing tags in .ui files using a stack-based approach.
"""

import os
import glob
import xml.etree.ElementTree as ET

def fix_ui_with_stack(file_path):
    """Fix missing </child> tags using a proper stack-based approach."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_lines = lines[:]
    fixed_lines = []
    tag_stack = []  # Stack of (tag_type, indent_level, line_number)
    
    for line_num, line in enumerate(lines):
        stripped = line.strip()
        current_indent = len(line) - len(line.lstrip())
        
        # Skip empty lines and comments
        if not stripped or stripped.startswith('<!--'):
            fixed_lines.append(line)
            continue
        
        # Handle opening tags
        if '<child' in line and not stripped.endswith('/>') and not '</child>' in line:
            # Opening child tag
            tag_stack.append(('child', current_indent, line_num))
            fixed_lines.append(line)
            
        elif '<object' in line and not stripped.endswith('/>'):
            # Opening object tag
            tag_stack.append(('object', current_indent, line_num))
            fixed_lines.append(line)
            
        elif '</object>' in stripped:
            # Closing object tag - need to close any child tags first
            while tag_stack and tag_stack[-1][0] == 'child':
                child_tag, child_indent, child_line = tag_stack.pop()
                # Insert closing child tag with correct indentation
                child_close_indent = ' ' * (child_indent)
                fixed_lines.append(child_close_indent + '</child>\n')
            
            # Remove the object from stack
            if tag_stack and tag_stack[-1][0] == 'object':
                tag_stack.pop()
                
            fixed_lines.append(line)
            
        elif '</child>' in stripped:
            # Explicit closing child tag
            if tag_stack and tag_stack[-1][0] == 'child':
                tag_stack.pop()
            fixed_lines.append(line)
            
        elif stripped.startswith('<placeholder'):
            # Placeholder - add it and close any open child
            fixed_lines.append(line)
            
        else:
            # Regular content line
            fixed_lines.append(line)
    
    # Close any remaining tags at the end
    while tag_stack:
        tag_type, indent, line_num = tag_stack.pop()
        if tag_type == 'child':
            close_indent = ' ' * indent
            fixed_lines.append(close_indent + '</child>\n')
    
    # Join lines and check if different
    new_content = ''.join(fixed_lines)
    original_content = ''.join(original_lines)
    
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Fixed {file_path}")
        return True
    else:
        print(f"  No changes needed for {file_path}")
        return False

def validate_xml(file_path):
    """Validate XML using xmllint."""
    import subprocess
    try:
        result = subprocess.run(['xmllint', '--noout', file_path], 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        return None, "xmllint not available"

def main():
    broken_files = [
        'bounds.ui', 'export_settings.ui', 'fonts.ui', 'log.ui', 
        'memory_analyzer.ui', 'model_extrusion.ui', 'model_plane_mirror.ui',
        'model_polygons.ui', 'model_position.ui', 'model_projection.ui',
        'model_rotation.ui', 'model_scaling.ui', 'model_support_distributed.ui',
        'model_support_grid.ui', 'model_support.ui', 'model_swap_axes.ui',
        'models.ui', 'opengl_view_dimension.ui', 'opengl_view_grid.ui',
        'parallel_processing.ui', 'processes.ui', 'progress_bar.ui',
        'pycam-project.ui', 'tasks.ui', 'toolpath_crop.ui', 'toolpath_export.ui',
        'toolpath_grid.ui', 'toolpath_simulation.ui', 'tools.ui'
    ]
    
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    fixed_count = 0
    valid_count = 0
    
    for filename in broken_files:
        file_path = os.path.join(ui_dir, filename)
        if os.path.exists(file_path):
            if fix_ui_with_stack(file_path):
                fixed_count += 1
            
            # Validate
            valid, error = validate_xml(file_path)
            if valid:
                valid_count += 1
                print(f"  ✓ {filename}: Valid XML")
            else:
                print(f"  ✗ {filename}: Invalid XML")
    
    print(f"\nSummary: Fixed {fixed_count} files, {valid_count} valid XML files")

if __name__ == "__main__":
    main()