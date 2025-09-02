#!/usr/bin/env python3

import os
import re
import glob

def convert_alignment_to_margins(file_path):
    """Convert GtkAlignment widgets to proper GTK 4 margin properties"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match GtkAlignment sections
    alignment_pattern = r'<object class="GtkAlignment"[^>]*>(.*?)</object>'
    
    def replace_alignment(match):
        alignment_content = match.group(1)
        
        # Extract padding/alignment properties
        left_padding = 0
        right_padding = 0
        top_padding = 0
        bottom_padding = 0
        xalign = 0.5
        yalign = 0.5
        
        # Parse existing properties
        padding_match = re.search(r'<property name="left_padding">([^<]+)</property>', alignment_content)
        if padding_match:
            left_padding = int(padding_match.group(1))
            
        padding_match = re.search(r'<property name="right_padding">([^<]+)</property>', alignment_content)
        if padding_match:
            right_padding = int(padding_match.group(1))
            
        padding_match = re.search(r'<property name="top_padding">([^<]+)</property>', alignment_content)
        if padding_match:
            top_padding = int(padding_match.group(1))
            
        padding_match = re.search(r'<property name="bottom_padding">([^<]+)</property>', alignment_content)
        if padding_match:
            bottom_padding = int(padding_match.group(1))
        
        # Extract child content
        child_match = re.search(r'<child>(.*?)</child>', alignment_content, re.DOTALL)
        if not child_match:
            return ""  # No child to preserve
        
        child_content = child_match.group(1).strip()
        
        # Find the child object and add margin properties to it
        object_match = re.search(r'(<object class="[^"]+"\s+id="[^"]*">)(.*?)(</object>)', child_content, re.DOTALL)
        if object_match:
            opening_tag = object_match.group(1)
            object_content = object_match.group(2)
            closing_tag = object_match.group(3)
            
            # Add margin properties
            margin_properties = ""
            if left_padding > 0:
                margin_properties += f'\n                <property name="margin-start">{left_padding}</property>'
            if right_padding > 0:
                margin_properties += f'\n                <property name="margin-end">{right_padding}</property>'
            if top_padding > 0:
                margin_properties += f'\n                <property name="margin-top">{top_padding}</property>'
            if bottom_padding > 0:
                margin_properties += f'\n                <property name="margin-bottom">{bottom_padding}</property>'
            
            # Add alignment properties if needed
            if xalign != 0.5:
                if xalign == 0:
                    margin_properties += '\n                <property name="halign">start</property>'
                elif xalign == 1:
                    margin_properties += '\n                <property name="halign">end</property>'
            
            if yalign != 0.5:
                if yalign == 0:
                    margin_properties += '\n                <property name="valign">start</property>'
                elif yalign == 1:
                    margin_properties += '\n                <property name="valign">end</property>'
            
            # Reconstruct the child object with margin properties
            new_child_content = opening_tag + object_content + margin_properties + '\n              ' + closing_tag
            return new_child_content
        
        return child_content  # Return as-is if we can't parse it
    
    # Replace all GtkAlignment instances
    modified_content = re.sub(alignment_pattern, replace_alignment, content, flags=re.DOTALL)
    
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
                
                if 'GtkAlignment' in original_content:
                    modified_content = convert_alignment_to_margins(ui_file)
                    
                    if modified_content != original_content:
                        with open(ui_file, 'w') as f:
                            f.write(modified_content)
                        print(f"✓ Fixed GtkAlignment in {os.path.basename(ui_file)}")
                        modified_files += 1
                    else:
                        print(f"- No alignment changes in {os.path.basename(ui_file)}")
                else:
                    print(f"- No GtkAlignment found in {os.path.basename(ui_file)}")
                    
            except Exception as e:
                print(f"✗ Error processing {ui_file}: {e}")
    
    print(f"\nFixed GtkAlignment in {modified_files} files")

if __name__ == "__main__":
    main()