#!/usr/bin/env python3
"""
Comprehensive script to fix missing </child> closing tags in .ui files.
"""

import os
import glob
import re

def fix_ui_file(file_path):
    """Fix missing </child> tags in a single .ui file."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply multiple passes to fix the patterns
    # Pass 1: Fix simple cases where </object> is followed by blank line and new <child>
    content = re.sub(
        r'(\s*</object>)\n\n(\s*)<child>',
        r'\1\n\2</child>\n\2<child>',
        content
    )
    
    # Pass 2: Fix cases where </object> is followed by blank line and parent </object>
    content = re.sub(
        r'(\s*</object>)\n\n(\s*)</object>',
        r'\1\n\2</child>\n\2</object>',
        content
    )
    
    # Pass 3: Fix placeholder cases
    content = re.sub(
        r'(\s*<placeholder/>)\n\n(\s*)</object>',
        r'\1\n\2</child>\n\2</object>',
        content
    )
    
    # Pass 4: Fix attributes cases
    content = re.sub(
        r'(\s*</attributes>)\n\n(\s*)</object>',
        r'\1\n\2</child>\n\2</object>',
        content
    )
    
    # Pass 5: Fix the specific case where there's a child type="label" after missing </child>
    content = re.sub(
        r'(\s*</object>)\n\n(\s*)<child type="label">',
        r'\1\n\2</child>\n\2<child type="label">',
        content
    )
    
    # Pass 6: Handle cases where interface is closing but child is still open
    content = re.sub(
        r'(\s*)</interface>\n(\s*)$',
        r'\1</child>\n\1</interface>\n',
        content
    )
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed {file_path}")
        return True
    else:
        print(f"  No changes needed for {file_path}")
        return False

def validate_xml(file_path):
    """Validate XML structure using xmllint if available."""
    import subprocess
    try:
        result = subprocess.run(['xmllint', '--noout', file_path], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except FileNotFoundError:
        return None, "xmllint not available"

def main():
    ui_dir = "/Users/charolastra/hack/pycam/share/ui"
    
    # List of files that need fixing (from the original problem statement)
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
    
    fixed_count = 0
    total_count = 0
    validation_results = {}
    
    for filename in broken_files:
        file_path = os.path.join(ui_dir, filename)
        if os.path.exists(file_path):
            total_count += 1
            if fix_ui_file(file_path):
                fixed_count += 1
            
            # Validate the fixed file
            valid, error = validate_xml(file_path)
            validation_results[filename] = (valid, error)
        else:
            print(f"Warning: {file_path} not found")
    
    print(f"\nSummary:")
    print(f"Fixed {fixed_count} out of {total_count} files.")
    
    print(f"\nValidation results:")
    valid_files = []
    invalid_files = []
    
    for filename, (valid, error) in validation_results.items():
        if valid is True:
            valid_files.append(filename)
            print(f"  ✓ {filename}: Valid XML")
        elif valid is False:
            invalid_files.append(filename)
            print(f"  ✗ {filename}: Invalid XML")
            if error:
                # Show just first line of error for brevity
                first_error = error.split('\n')[0]
                print(f"    Error: {first_error}")
        else:
            print(f"  ? {filename}: Could not validate (xmllint not available)")
    
    print(f"\nFinal summary: {len(valid_files)} valid, {len(invalid_files)} invalid")
    
    return len(invalid_files) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)