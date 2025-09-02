#!/usr/bin/env python3
"""
Simple pattern-based fixer for missing </child> tags.
Based on the exact pattern observed in the broken files.
"""

import os
import re

def fix_simple_pattern(file_path):
    """Fix the specific pattern of missing </child> tags."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: </object> followed by blank lines and <child>
    # This means the previous child wasn't closed
    content = re.sub(
        r'(\s*</object>)\n\n(\s*<child)',
        r'\1\n\2</child>\n\2',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 2: </object> followed by blank lines and </object>
    # This means the previous child wasn't closed  
    content = re.sub(
        r'(\s*</object>)\n\n(\s*</object>)',
        r'\1\n\2</child>\n\2',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 3: <placeholder/> followed by blank lines and </object>
    content = re.sub(
        r'(\s*<placeholder/>)\n\n(\s*</object>)',
        r'\1\n\2</child>\n\2',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 4: </attributes> followed by blank lines and </object>
    content = re.sub(
        r'(\s*</attributes>)\n\n(\s*</object>)',
        r'\1\n\2</child>\n\2',
        content,
        flags=re.MULTILINE
    )

    # Pattern 5: Handle interface closing
    content = re.sub(
        r'(\s*</object>)\n\n(\s*</interface>)',
        r'\1\n\2</child>\n\2',
        content,
        flags=re.MULTILINE
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
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
    invalid_count = 0
    
    for filename in broken_files:
        file_path = os.path.join(ui_dir, filename)
        if os.path.exists(file_path):
            if fix_simple_pattern(file_path):
                fixed_count += 1
            
            # Validate
            valid, error = validate_xml(file_path)
            if valid:
                valid_count += 1
                print(f"  ✓ {filename}: Valid XML")
            elif valid is False:
                invalid_count += 1
                print(f"  ✗ {filename}: Invalid XML")
                # Show first error line
                if error:
                    first_line = error.split('\n')[0]
                    print(f"    {first_line}")
    
    print(f"\nSUMMARY:")
    print(f"Fixed: {fixed_count} files")
    print(f"Valid: {valid_count} files") 
    print(f"Invalid: {invalid_count} files")
    
    if valid_count > 0:
        print(f"\nSUCCESS: Fixed {valid_count} files with valid XML!")
    
    return valid_count > 0

if __name__ == "__main__":
    main()