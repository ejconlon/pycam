#!/usr/bin/env python3

import os
import re
import glob

def update_gtk_version_requirements(file_path):
    """Update GTK version requirements from 3.x to 4.0"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Update GTK version requirement
    content = re.sub(r'<requires lib="gtk\+" version="3\.\d+"/>', 
                     '<requires lib="gtk" version="4.0"/>', content)
    
    return content

def fix_deprecated_properties(content):
    """Fix deprecated GTK properties for GTK 4"""
    
    # Remove deprecated properties
    deprecated_props = [
        r'[ \t]*<property name="shadow_type".*?</property>\n',
        r'[ \t]*<property name="border_width".*?</property>\n',
        r'[ \t]*<property name="use_action_appearance".*?</property>\n',
        r'[ \t]*<property name="related_action".*?</property>\n',
    ]
    
    for prop_pattern in deprecated_props:
        content = re.sub(prop_pattern, '', content)
    
    # Fix property name changes
    property_changes = {
        'xalign': 'halign',  # Only in specific contexts
        'yalign': 'valign',  # Only in specific contexts
        'stock': 'icon-name',  # For some cases
    }
    
    # Be careful with xalign/yalign - only change in appropriate contexts
    # Don't change them in GtkLabel contexts where they're still valid
    
    return content

def fix_stock_properties(content):
    """Convert deprecated stock properties to icon-name"""
    
    # Common stock to icon-name mappings
    stock_mappings = {
        'gtk-execute': 'system-run',
        'gtk-about': 'help-about',
        'gtk-quit': 'application-exit',
        'gtk-open': 'document-open',
        'gtk-save': 'document-save',
        'gtk-save-as': 'document-save-as',
        'gtk-undo': 'edit-undo',
        'gtk-redo': 'edit-redo',
        'gtk-cut': 'edit-cut',
        'gtk-copy': 'edit-copy',
        'gtk-paste': 'edit-paste',
        'gtk-delete': 'edit-delete',
        'gtk-preferences': 'preferences-system',
        'gtk-help': 'help-browser',
    }
    
    for stock_id, icon_name in stock_mappings.items():
        content = re.sub(f'<property name="stock">{stock_id}</property>',
                        f'<property name="icon-name">{icon_name}</property>', content)
        content = re.sub(f'<property name="stock_id">{stock_id}</property>',
                        f'<property name="icon-name">{icon_name}</property>', content)
    
    return content

def remove_gtkaction_objects(content):
    """Remove GtkAction objects which are deprecated in GTK 4"""
    
    # Remove entire GtkAction object blocks
    action_pattern = r'<object class="GtkAction"[^>]*>.*?</object>\n'
    content = re.sub(action_pattern, '', content, flags=re.DOTALL)
    
    # Remove GtkToggleAction objects too
    toggle_action_pattern = r'<object class="GtkToggleAction"[^>]*>.*?</object>\n'
    content = re.sub(toggle_action_pattern, '', content, flags=re.DOTALL)
    
    return content

def fix_other_compatibility_issues(content):
    """Fix various other GTK 4 compatibility issues"""
    
    # Fix resize_mode property (deprecated in GTK 4)
    content = re.sub(r'[ \t]*<property name="resize_mode".*?</property>\n', '', content)
    
    # Fix window type hints (some are deprecated)
    content = re.sub(r'<property name="type_hint">utility</property>',
                     '<property name="type_hint">dialog</property>', content)
    
    # Fix deprecated packing properties in some contexts
    # Note: This is complex and context-dependent, so we'll be conservative
    
    return content

def main():
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    modified_count = 0
    
    for ui_file in ui_files:
        if ui_file.endswith('.ui'):
            print(f"Processing {os.path.basename(ui_file)}")
            
            try:
                with open(ui_file, 'r') as f:
                    original_content = f.read()
                
                # Apply fixes
                content = original_content
                content = update_gtk_version_requirements(content)
                content = fix_deprecated_properties(content)
                content = fix_stock_properties(content)
                content = remove_gtkaction_objects(content)
                content = fix_other_compatibility_issues(content)
                
                if content != original_content:
                    # Validate XML before saving
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
                        tmp.write(content)
                        tmp.flush()
                        
                        # Test XML validity
                        result = os.system(f'xmllint --noout "{tmp.name}" 2>/dev/null')
                        os.unlink(tmp.name)
                        
                        if result == 0:  # XML is valid
                            with open(ui_file, 'w') as f:
                                f.write(content)
                            print(f"✓ Updated {os.path.basename(ui_file)}")
                            modified_count += 1
                        else:
                            print(f"⚠ Skipped {os.path.basename(ui_file)} - would create invalid XML")
                else:
                    print(f"- No changes needed for {os.path.basename(ui_file)}")
                    
            except Exception as e:
                print(f"✗ Error processing {ui_file}: {e}")
    
    print(f"\nUpdated {modified_count} files for GTK 4 compatibility")

if __name__ == "__main__":
    main()