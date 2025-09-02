#!/usr/bin/env python3
"""
Remove deprecated shadow_type properties from GTK 4 UI files.
These properties can cause sizing calculation issues including negative width warnings.
"""

import re
import os
from pathlib import Path

def remove_shadow_type(content):
    """Remove shadow_type property lines from UI content."""
    # Match the entire property line with proper indentation and newline
    pattern = r'[ \t]*<property name="shadow_type">.*?</property>\n'
    return re.sub(pattern, '', content)

def process_ui_file(filepath):
    """Process a single UI file to remove shadow_type properties."""
    print(f"Processing {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = remove_shadow_type(original_content)
        
        if original_content != fixed_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✓ Fixed {filepath}")
            return True
        else:
            print(f"- No changes needed for {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Remove shadow_type properties from all UI files."""
    ui_dir = Path('/Users/charolastra/hack/pycam/share/ui')
    
    # Get all .ui files that are not backups or working files
    ui_files = []
    for ui_file in ui_dir.glob('*.ui'):
        if 'backup' not in ui_file.name and 'working' not in ui_file.name:
            ui_files.append(ui_file)
    
    fixed_count = 0
    total_count = len(ui_files)
    
    print(f"Found {total_count} UI files to process...")
    
    for ui_file in sorted(ui_files):
        if process_ui_file(ui_file):
            fixed_count += 1
    
    print(f"\nSummary: Fixed {fixed_count}/{total_count} files")
    print("Removed deprecated shadow_type properties that can cause GTK 4 sizing issues.")

if __name__ == '__main__':
    main()