#!/usr/bin/env python3

import os
import re
import glob
import subprocess

def update_remaining_gtk3_files():
    """Update remaining files that still use GTK 3 requirements"""
    
    ui_files = glob.glob("/Users/charolastra/hack/pycam/share/ui/*.ui")
    
    for ui_file in ui_files:
        with open(ui_file, 'r') as f:
            content = f.read()
        
        # Check if it still uses GTK 3
        if 'requires lib="gtk+" version="3' in content or 'requires lib="gtk+" version="3' in content:
            print(f"Updating {os.path.basename(ui_file)}")
            
            # Update GTK version requirement
            content = re.sub(r'<requires lib="gtk\+" version="3\.\d+"\s*/>', 
                             '<requires lib="gtk" version="4.0"/>', content)
            content = re.sub(r'<requires lib="gtk\+" version="3\.\d+"/>', 
                             '<requires lib="gtk" version="4.0"/>', content)
            
            # Write back
            with open(ui_file, 'w') as f:
                f.write(content)
            
            # Validate
            result = subprocess.run(['xmllint', '--noout', ui_file], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Successfully updated {os.path.basename(ui_file)}")
            else:
                print(f"⚠ Warning: {os.path.basename(ui_file)} may have validation issues")

if __name__ == "__main__":
    update_remaining_gtk3_files()