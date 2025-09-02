#!/usr/bin/env python3

import os
import re
import glob

def fix_tab_labels(file_path):
    """Add minimum width properties to tab labels in GtkNotebook widgets"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match tab labels within GtkNotebookPage
    tab_label_pattern = r'(<property name="tab">\s*<object class="GtkLabel"[^>]*>)(.*?)(</object>\s*</property>)'
    
    def add_width_property(match):
        opening_section = match.group(1)
        properties_section = match.group(2)
        closing_section = match.group(3)
        
        # Check if width-request is already present
        if 'width-request' not in properties_section:
            # Add width-request property
            width_property = '\n                    <property name="width-request">50</property>'
            properties_section = properties_section + width_property
        
        return opening_section + properties_section + closing_section
    
    modified_content = re.sub(tab_label_pattern, add_width_property, content, flags=re.DOTALL)
    
    # Also check for direct tab label usage in notebook children
    notebook_label_pattern = r'(<object class="GtkLabel"[^>]*>)((?:(?!</object>).)*label[^>]*>((?:(?!</property>).)*)</property>)((?:(?!</object>.)*)</object>)'
    
    def add_width_to_labels(match):
        opening_tag = match.group(1)
        content_section = match.group(2) + match.group(3) + match.group(4)
        
        # Only modify if this is within a notebook context and doesn't already have width-request
        if 'width-request' not in content_section:
            # Add width-request before the closing tag
            width_property = '\n    <property name="width-request">50</property>'
            content_section = content_section.replace('</object>', width_property + '\n    </object>')
        
        return opening_tag + content_section
    
    # Apply to labels that might be tab labels (more conservative approach)
    return modified_content

def main():
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    modified_files = 0
    
    for ui_file in ui_files:
        if ui_file.endswith('.ui'):
            print(f"Processing {os.path.basename(ui_file)}")
            
            try:
                with open(ui_file, 'r') as f:
                    original_content = f.read()
                
                modified_content = fix_tab_labels(ui_file)
                
                if modified_content != original_content:
                    with open(ui_file, 'w') as f:
                        f.write(modified_content)
                    print(f"✓ Updated {os.path.basename(ui_file)}")
                    modified_files += 1
                else:
                    print(f"- No changes needed for {os.path.basename(ui_file)}")
                    
            except Exception as e:
                print(f"✗ Error processing {ui_file}: {e}")
    
    print(f"\nModified {modified_files} files")

if __name__ == "__main__":
    main()