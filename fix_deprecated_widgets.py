#!/usr/bin/env python3

import os
import re
import glob
import subprocess

def fix_deprecated_widgets(file_path):
    """Fix deprecated GTK 4 widgets"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Replace GtkButtonBox with GtkBox
    content = re.sub(r'<object class="GtkButtonBox"', '<object class="GtkBox"', content)
    
    # Replace GtkButtonBox properties
    content = re.sub(r'<property name="layout_style">[^<]*</property>', 
                     '<property name="spacing">5</property>', content)
    
    # Fix other deprecated widgets
    # GtkComboBoxText -> GtkComboBox (if needed)
    # GtkTable -> GtkGrid (already done by earlier scripts)
    
    # Remove some deprecated properties
    deprecated_properties = [
        r'<property name="stock_size">[^<]*</property>',
        r'<property name="use_action_appearance">[^<]*</property>',
        r'<property name="related_action">[^<]*</property>',
    ]
    
    for prop_pattern in deprecated_properties:
        content = re.sub(prop_pattern, '', content)
    
    return content if content != original else None

def validate_xml(file_path):
    """Validate XML using xmllint"""
    try:
        result = subprocess.run(['xmllint', '--noout', file_path], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    modified_count = 0
    
    for ui_file in ui_files:
        print(f"Processing {os.path.basename(ui_file)}")
        
        try:
            updated_content = fix_deprecated_widgets(ui_file)
            
            if updated_content:
                # Create backup
                backup_path = ui_file + '.backup'
                with open(ui_file, 'r') as f:
                    with open(backup_path, 'w') as backup:
                        backup.write(f.read())
                
                # Write updated content
                with open(ui_file, 'w') as f:
                    f.write(updated_content)
                
                # Validate
                if validate_xml(ui_file):
                    print(f"✓ Updated {os.path.basename(ui_file)}")
                    os.remove(backup_path)
                    modified_count += 1
                else:
                    print(f"⚠ Restored {os.path.basename(ui_file)} - XML validation failed")
                    # Restore from backup
                    with open(backup_path, 'r') as backup:
                        with open(ui_file, 'w') as f:
                            f.write(backup.read())
                    os.remove(backup_path)
            else:
                print(f"- No changes needed for {os.path.basename(ui_file)}")
                    
        except Exception as e:
            print(f"✗ Error processing {ui_file}: {e}")
    
    print(f"\nUpdated {modified_count} files")

if __name__ == "__main__":
    main()