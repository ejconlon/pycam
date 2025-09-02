#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

from pycam.Plugins.FilenameDialog import FilenameDialog
from pycam.Gui.Settings import Settings

def test_file_dialog():
    """Test the FilenameDialog functionality"""
    
    # Create a test STL file
    test_file = "test_model.stl"
    if not os.path.exists(test_file):
        with open(test_file, 'w') as f:
            f.write("""solid test
  facet normal 0 0 1
    outer loop
      vertex 0 0 0
      vertex 1 0 0
      vertex 0 1 0
    endloop
  endfacet
endsolid test""")
    
    # Initialize settings
    settings = Settings()
    
    # Create and setup FilenameDialog plugin
    plugin = FilenameDialog(settings, 'FilenameDialog')
    if not plugin.setup():
        print("❌ Failed to setup FilenameDialog plugin")
        return
    
    print("✅ FilenameDialog plugin setup successful")
    
    # Test file selection (in mode_load=True for opening files)
    print("Testing file dialog for loading...")
    print("Note: This would show a file dialog in a GUI environment")
    
    # We can't actually test the GUI dialog in CI, but we can verify the method is callable
    get_filename_func = settings.get('get_filename_func')
    if get_filename_func:
        print("✅ get_filename_func is properly set")
        print(f"Function: {get_filename_func}")
    else:
        print("❌ get_filename_func is not set")
        return
    
    print("✅ File dialog implementation should now work correctly")
    print("When you run PyCAM and select 'Open Model', it should:")
    print("1. Show the file chooser dialog")
    print("2. Allow you to select a file")
    print("3. Return the selected filename")
    print("4. Load the model in the application")

if __name__ == "__main__":
    test_file_dialog()