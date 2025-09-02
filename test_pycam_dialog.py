#!/usr/bin/env python3
"""Test PyCAM's file dialog integration"""

import sys
import os
sys.path.insert(0, '/Users/charolastra/hack/pycam')

# Set up GTK
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

# Test the FilenameDialog plugin directly
try:
    from pycam.Plugins.FilenameDialog import FilenameDialog
    
    # Mock core/event manager
    class MockCore:
        def __init__(self):
            self.data = {}
            
        def set(self, key, value):
            self.data[key] = value
            
        def get(self, key):
            return self.data.get(key)
    
    # Create test environment
    core = MockCore()
    filename_dialog = FilenameDialog(core, "FilenameDialog")
    
    print("✓ FilenameDialog plugin created successfully")
    
    # Test setup
    filename_dialog.gui = True  # Mock GUI
    setup_result = filename_dialog.setup()
    print(f"✓ Setup result: {setup_result}")
    
    # Check if get_filename_func was registered
    get_filename_func = core.get("get_filename_func")
    if get_filename_func:
        print("✓ get_filename_func registered successfully")
        print(f"  Function: {get_filename_func}")
        
        # Try to test call (but don't actually show dialog)
        print("✓ File dialog should work when called from PyCAM menu")
    else:
        print("✗ get_filename_func not registered")
        
except Exception as e:
    print(f"✗ Error testing FilenameDialog: {e}")
    import traceback
    traceback.print_exc()