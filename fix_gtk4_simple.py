#!/usr/bin/env python3

import os
import re
import glob
import subprocess

def update_gtk_requirements_only(file_path):
    """Update only GTK version requirements and basic fixes"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Update GTK version requirement
    content = re.sub(r'<requires lib="gtk\+" version="3\.\d+"/>', 
                     '<requires lib="gtk" version="4.0"/>', content)
    
    # Remove GtkAction objects (deprecated in GTK 4)
    content = re.sub(r'  <object class="GtkAction"[^>]*>.*?</object>\n', '', content, flags=re.DOTALL)
    content = re.sub(r'  <object class="GtkToggleAction"[^>]*>.*?</object>\n', '', content, flags=re.DOTALL)
    
    # Fix some basic deprecated properties
    content = re.sub(r'    <property name="border_width">.*?</property>\n', '', content)
    content = re.sub(r'    <property name="resize_mode">.*?</property>\n', '', content)
    
    # Convert basic stock properties
    stock_mappings = {
        'gtk-execute': 'system-run',
        'gtk-about': 'help-about',
        'gtk-undo': 'edit-undo',
    }
    
    for stock_id, icon_name in stock_mappings.items():
        content = re.sub(f'<property name="stock">{stock_id}</property>',
                        f'<property name="icon-name">{icon_name}</property>', content)
    
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
            updated_content = update_gtk_requirements_only(ui_file)
            
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
                    os.remove(backup_path)  # Remove backup if successful
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