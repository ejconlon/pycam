#!/usr/bin/env python3
"""
Test the full menu loading process similar to PyCAM
"""

import os
import sys

# Add pycam to path  
sys.path.insert(0, '/Users/charolastra/hack/pycam')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gio, GLib

def test_full_menu_setup():
    print("=== Testing Full Menu Setup ===")
    
    # Create a builder and load the UI file
    builder = Gtk.Builder()
    ui_file = "/Users/charolastra/hack/pycam/share/ui/pycam-project-functional.ui"
    
    try:
        print("Loading UI file...")
        builder.add_from_file(ui_file)
        print("✅ UI file loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load UI file: {e}")
        return False
        
    # Get the MenuBar widget
    try:
        menubar_widget = builder.get_object("MenuBar")
        print(f"✅ MenuBar widget found: {menubar_widget}")
        print(f"   Type: {type(menubar_widget)}")
    except Exception as e:
        print(f"❌ Failed to get MenuBar widget: {e}")
        return False
        
    # Create a menu model
    print("Creating menu model...")
    menubar_model = Gio.Menu()
    file_menu = Gio.Menu()
    file_menu.append("_Open Model...", "app.open-model")
    menubar_model.append_submenu("_File", file_menu)
    
    # Try to set the menu model
    try:
        print("Setting menu model on MenuBar widget...")
        menubar_widget.set_menu_model(menubar_model)
        print("✅ Menu model set successfully")
    except Exception as e:
        print(f"❌ Failed to set menu model: {e}")
        return False
        
    # Create actions
    print("Creating actions...")
    action_group = Gio.SimpleActionGroup()
    action = Gio.SimpleAction.new("open-model", None)
    action.connect("activate", lambda a, p: print("🎉 Open Model action triggered!"))
    action_group.add_action(action)
    
    # Get the main window 
    try:
        window = builder.get_object("ProjectWindow")
        print(f"✅ Main window found: {window}")
        print(f"   Type: {type(window)}")
        
        # Add action group to window
        window.insert_action_group("app", action_group)
        print("✅ Action group added to window")
        
    except Exception as e:
        print(f"❌ Failed to get main window or add actions: {e}")
        return False
        
    print("✅ Full menu setup completed successfully!")
    return True

def test_minimal_window():
    print("\n=== Testing Minimal Window Display ===")
    
    # Create a simple application window with menu
    window = Gtk.ApplicationWindow()
    window.set_title("Menu Test")
    window.set_default_size(400, 300)
    
    # Create menu bar
    menubar_widget = Gtk.PopoverMenuBar()
    
    # Create menu model
    menubar_model = Gio.Menu()
    file_menu = Gio.Menu()
    file_menu.append("_Test Item", "app.test")
    menubar_model.append_submenu("_File", file_menu)
    
    # Set menu model
    menubar_widget.set_menu_model(menubar_model)
    
    # Create layout
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box.append(menubar_widget)
    
    label = Gtk.Label(label="Menu should appear above")
    box.append(label)
    
    window.set_child(box)
    
    # Create action
    action_group = Gio.SimpleActionGroup()
    action = Gio.SimpleAction.new("test", None)
    action.connect("activate", lambda a, p: print("🎉 Test action triggered!"))
    action_group.add_action(action)
    window.insert_action_group("app", action_group)
    
    print("Created minimal window with menu")
    print("Window has menu bar:", menubar_widget is not None)
    print("Menu model has items:", menubar_model.get_n_items() > 0)
    
    return True

if __name__ == "__main__":
    try:
        success1 = test_full_menu_setup()
        success2 = test_minimal_window()
        
        if success1 and success2:
            print("\n🎉 All tests passed! Menu setup should work.")
        else:
            print("\n❌ Some tests failed.")
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()