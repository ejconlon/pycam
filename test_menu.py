#!/usr/bin/env python3
"""
Simple test to verify the File menu functionality can work
"""

import os
import sys

# Add pycam to path  
sys.path.insert(0, '/Users/charolastra/hack/pycam')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gio

# Test if basic menu creation works
def test_menu_creation():
    print("Testing basic menu creation...")
    
    # Create a simple menu
    menu = Gio.Menu()
    file_menu = Gio.Menu()
    file_menu.append("_Open Model...", "app.open-model")
    menu.append_submenu("_File", file_menu)
    
    print(f"Menu created with {menu.get_n_items()} items")
    print(f"File submenu created with {file_menu.get_n_items()} items")
    
    # Create a simple action
    action = Gio.SimpleAction.new("open-model", None) 
    action.connect("activate", lambda a, p: print("Open Model action triggered!"))
    
    print("Action created successfully")
    return True

def test_ui_file_exists():
    print("Testing if UI file exists...")
    
    ui_file_path = "/Users/charolastra/hack/pycam/share/ui/pycam-project-functional.ui"
    
    if os.path.exists(ui_file_path):
        print(f"✅ UI file exists: {ui_file_path}")
        
        # Check if it has MenuBar
        with open(ui_file_path, 'r') as f:
            content = f.read()
            if 'id="MenuBar"' in content:
                print("✅ MenuBar widget found in UI file")
            else:
                print("❌ MenuBar widget NOT found in UI file")
                
            if 'GtkPopoverMenuBar' in content:
                print("✅ GtkPopoverMenuBar found in UI file")
            else:
                print("❌ GtkPopoverMenuBar NOT found in UI file")
                
        return True
    else:
        print(f"❌ UI file does not exist: {ui_file_path}")
        return False

if __name__ == "__main__":
    print("=== Testing PyCAM Menu System ===")
    
    try:
        test_menu_creation()
        test_ui_file_exists()
        print("=== Test completed ===")
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()