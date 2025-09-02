#!/usr/bin/env python3

"""
Script to fix XML tag mismatches in .ui files by adding missing </child> closing tags.
"""

import os
import re
import sys
from pathlib import Path

def fix_xml_tags(content):
    """
    Fix XML by adding missing </child> closing tags.
    
    The pattern is:
    - <child> opens
    - <object> opens 
    - ... properties ...
    - </object> closes
    - Missing </child> - this is what we need to add
    """
    lines = content.split('\n')
    fixed_lines = []
    stack = []  # Track open tags with their indentation
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        
        # Track opening tags
        if '<child>' in stripped and not '<child ' in stripped:
            stack.append(('child', indent, i))
            fixed_lines.append(line)
        elif '<object ' in stripped and not '</object>' in stripped:
            # Get class name for tracking
            match = re.search(r'class="([^"]*)"', stripped)
            obj_class = match.group(1) if match else 'object'
            stack.append(('object', indent, i, obj_class))
            fixed_lines.append(line)
        elif '</object>' in stripped:
            # Close object and check if we need to close child
            fixed_lines.append(line)
            
            # Remove the object from stack
            if stack and stack[-1][0] == 'object':
                stack.pop()
                
            # Check if the next non-empty line starts a new child or closes current level
            next_line_idx = i + 1
            while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                next_line_idx += 1
                
            if next_line_idx < len(lines):
                next_line = lines[next_line_idx]
                next_stripped = next_line.strip()
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # If we have an open child and the next element is at same or lower indent
                # and it's not another child at the same level, close the child
                if (stack and stack[-1][0] == 'child' and 
                    (next_indent <= stack[-1][1] or 
                     next_stripped.startswith('</') or
                     (next_stripped.startswith('<child>') and next_indent <= stack[-1][1]))):
                    
                    child_indent = stack[-1][1]
                    fixed_lines.append(' ' * (child_indent + 2) + '</child>')
                    stack.pop()
        else:
            fixed_lines.append(line)
    
    # Close any remaining open child tags
    while stack:
        if stack[-1][0] == 'child':
            child_indent = stack[-1][1]
            fixed_lines.append(' ' * (child_indent + 2) + '</child>')
        stack.pop()
    
    return '\n'.join(fixed_lines)

def fix_ui_file(filepath):
    """Fix a single .ui file."""
    print(f"Fixing {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_xml_tags(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print(f"✓ Fixed {filepath}")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing {filepath}: {e}")
        return False

def main():
    """Main function to fix all broken .ui files."""
    ui_dir = Path('/Users/charolastra/hack/pycam/share/ui')
    
    # List of files that were identified as broken
    broken_files = [
        'bounds.ui', 'export_settings.ui', 'fonts.ui', 'log.ui', 
        'memory_analyzer.ui', 'model_extrusion.ui', 'model_plane_mirror.ui',
        'model_polygons.ui', 'model_position.ui', 'model_projection.ui', 
        'model_rotation.ui', 'model_scaling.ui', 'model_support_distributed.ui',
        'model_support_grid.ui', 'model_support.ui', 'model_swap_axes.ui',
        'models.ui', 'opengl_view_dimension.ui', 'opengl_view_grid.ui',
        'parallel_processing.ui', 'processes.ui', 'progress_bar.ui', 
        'pycam-project.ui', 'tasks.ui', 'toolpath_crop.ui', 
        'toolpath_export.ui', 'toolpath_grid.ui', 'toolpath_simulation.ui',
        'tools.ui'
    ]
    
    success_count = 0
    
    for filename in broken_files:
        filepath = ui_dir / filename
        if filepath.exists():
            if fix_ui_file(filepath):
                success_count += 1
        else:
            print(f"File not found: {filepath}")
    
    print(f"\nSummary: {success_count}/{len(broken_files)} files fixed successfully")
    return success_count == len(broken_files)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)