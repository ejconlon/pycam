#!/usr/bin/env python3

import os
import re
import glob

def fix_notebook_tabs(file_path):
    """Add minimum tab sizing properties to GtkNotebook widgets"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match GtkNotebook objects
    notebook_pattern = r'(<object class="GtkNotebook"[^>]*>)'
    
    def add_tab_properties(match):
        opening_tag = match.group(1)
        # Check if we already have show-tabs property
        return opening_tag
    
    # Find notebook objects and add tab properties after them
    notebook_sections = re.finditer(r'(<object class="GtkNotebook"[^>]*>)(.*?)(</object>)', content, re.DOTALL)
    
    modified_content = content
    offset = 0
    
    for match in notebook_sections:
        start_pos = match.start(2) + offset
        properties_section = match.group(2)
        
        # Check if we already have show-tabs or tab properties
        if 'show-tabs' not in properties_section and 'tab_show_border' not in properties_section:
            # Add tab visibility and sizing properties
            tab_properties = '''    <property name="show-tabs">true</property>
    <property name="scrollable">true</property>
    <property name="enable-popup">true</property>
'''
            
            # Find where to insert (after existing properties, before first child)
            child_match = re.search(r'\n\s*<child', properties_section)
            comment_match = re.search(r'\n\s*<!--', properties_section)
            
            insert_pos = start_pos
            if child_match:
                insert_pos = start_pos + child_match.start()
            elif comment_match:
                insert_pos = start_pos + comment_match.start()
            else:
                # Insert before closing </object>
                insert_pos = match.end(2) + offset
            
            modified_content = modified_content[:insert_pos] + '\n' + tab_properties + modified_content[insert_pos:]
            offset += len(tab_properties) + 1
    
    return modified_content

def main():
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    for ui_file in ui_files:
        if ui_file.endswith('.ui'):
            print(f"Processing {os.path.basename(ui_file)}")
            
            try:
                modified_content = fix_notebook_tabs(ui_file)
                
                if modified_content:
                    with open(ui_file, 'w') as f:
                        f.write(modified_content)
                    print(f"✓ Updated {os.path.basename(ui_file)}")
                else:
                    print(f"- No changes needed for {os.path.basename(ui_file)}")
                    
            except Exception as e:
                print(f"✗ Error processing {ui_file}: {e}")

if __name__ == "__main__":
    main()