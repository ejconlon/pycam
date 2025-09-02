#!/usr/bin/env python3

import os
import re
import glob
from xml.etree import ElementTree as ET

def fix_alignment_in_file(file_path):
    """Fix GtkAlignment usage by converting to proper GTK 4 structure"""
    
    try:
        # Parse the XML
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        changed = False
        
        # Find all GtkAlignment objects
        for alignment in root.findall(".//object[@class='GtkAlignment']"):
            changed = True
            parent = None
            
            # Find the parent element
            for elem in root.iter():
                if alignment in elem:
                    parent = elem
                    break
            
            if parent is None:
                continue
            
            # Extract properties from GtkAlignment
            margin_start = 0
            margin_end = 0  
            margin_top = 0
            margin_bottom = 0
            halign = "fill"
            valign = "fill"
            
            for prop in alignment.findall("property"):
                prop_name = prop.get("name")
                prop_value = prop.text
                
                if prop_name == "left_padding":
                    margin_start = int(prop_value or 0)
                elif prop_name == "right_padding":
                    margin_end = int(prop_value or 0)
                elif prop_name == "top_padding":
                    margin_top = int(prop_value or 0)
                elif prop_name == "bottom_padding":
                    margin_bottom = int(prop_value or 0)
                elif prop_name == "xalign":
                    xalign_val = float(prop_value or 0.5)
                    if xalign_val <= 0.1:
                        halign = "start"
                    elif xalign_val >= 0.9:
                        halign = "end"
                    else:
                        halign = "center"
                elif prop_name == "yalign":
                    yalign_val = float(prop_value or 0.5)
                    if yalign_val <= 0.1:
                        valign = "start"
                    elif yalign_val >= 0.9:
                        valign = "end"
                    else:
                        valign = "center"
            
            # Find the child element of GtkAlignment
            child_elem = alignment.find("child")
            if child_elem is not None:
                child_object = child_elem.find("object")
                if child_object is not None:
                    # Add margin and alignment properties to the child object
                    if margin_start > 0:
                        margin_prop = ET.Element("property", name="margin-start")
                        margin_prop.text = str(margin_start)
                        child_object.insert(0, margin_prop)
                    
                    if margin_end > 0:
                        margin_prop = ET.Element("property", name="margin-end")
                        margin_prop.text = str(margin_end)
                        child_object.insert(0, margin_prop)
                    
                    if margin_top > 0:
                        margin_prop = ET.Element("property", name="margin-top")
                        margin_prop.text = str(margin_top)
                        child_object.insert(0, margin_prop)
                    
                    if margin_bottom > 0:
                        margin_prop = ET.Element("property", name="margin-bottom")
                        margin_prop.text = str(margin_bottom)
                        child_object.insert(0, margin_prop)
                    
                    if halign != "fill":
                        halign_prop = ET.Element("property", name="halign")
                        halign_prop.text = halign
                        child_object.insert(0, halign_prop)
                    
                    if valign != "fill":
                        valign_prop = ET.Element("property", name="valign")
                        valign_prop.text = valign
                        child_object.insert(0, valign_prop)
                    
                    # Replace GtkAlignment with its child in the parent
                    parent.remove(alignment)
                    parent.append(child_object)
                    
                    # If there was a packing element, preserve it
                    packing = child_elem.find("packing")
                    if packing is not None:
                        new_packing = ET.Element("packing")
                        for pack_prop in packing:
                            new_packing.append(pack_prop)
                        parent.append(new_packing)
        
        # Also remove shadow_type properties while we're at it
        for obj in root.findall(".//object"):
            for prop in obj.findall("property[@name='shadow_type']"):
                obj.remove(prop)
                changed = True
        
        if changed:
            # Write the modified XML back
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    modified_count = 0
    
    for ui_file in ui_files:
        if ui_file.endswith('.ui'):
            print(f"Processing {os.path.basename(ui_file)}")
            
            # Check if file contains GtkAlignment
            with open(ui_file, 'r') as f:
                content = f.read()
                
            if 'GtkAlignment' in content:
                if fix_alignment_in_file(ui_file):
                    print(f"✓ Fixed GtkAlignment in {os.path.basename(ui_file)}")
                    modified_count += 1
                else:
                    print(f"- No changes made to {os.path.basename(ui_file)}")
            else:
                print(f"- No GtkAlignment found in {os.path.basename(ui_file)}")
    
    print(f"\nFixed {modified_count} files")

if __name__ == "__main__":
    main()