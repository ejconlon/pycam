#!/usr/bin/env python3

import os
import sys
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio

# Add the pycam path for imports
sys.path.insert(0, '/Users/charolastra/hack/pycam')

import pycam.Utils

def test_file_dialog_filters():
    """Test GTK 4 FileDialog with filters"""
    
    app = Gtk.Application()
    
    def on_activate(app):
        window = Gtk.ApplicationWindow(application=app)
        window.set_title("File Dialog Filter Test")
        window.set_default_size(300, 200)
        
        button = Gtk.Button(label="Open File Dialog")
        button.connect("clicked", on_button_clicked, window)
        window.set_child(button)
        
        window.present()
    
    def on_button_clicked(button, parent_window):
        # Create FileDialog
        dialog = Gtk.FileDialog()
        dialog.set_title("Test File Dialog")
        
        # Create filters like FilenameDialog does
        filter_store = Gio.ListStore.new(Gtk.FileFilter)
        
        # Create STL filter
        stl_filter = Gtk.FileFilter()
        stl_filter.set_name("STL models")
        
        # Add pattern
        stl_pattern = pycam.Utils.get_case_insensitive_file_pattern("*.stl")
        print(f"Adding STL pattern: {stl_pattern}")
        stl_filter.add_pattern(stl_pattern)
        
        # Try different approach - add basic pattern too
        stl_filter.add_pattern("*.stl")
        stl_filter.add_pattern("*.STL")
        
        # Add mime type
        stl_filter.add_mime_type("model/stl")
        # Try alternative mime types
        stl_filter.add_mime_type("application/sla")
        
        filter_store.append(stl_filter)
        
        # Create All files filter
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")
        filter_store.append(all_filter)
        
        # Set filters
        dialog.set_filters(filter_store)
        dialog.set_default_filter(filter_store.get_item(0))
        
        def on_dialog_response(dialog, result):
            try:
                file = dialog.open_finish(result)
                if file:
                    print(f"Selected file: {file.get_path()}")
                else:
                    print("No file selected")
            except Exception as e:
                print(f"Dialog cancelled or error: {e}")
            app.quit()
        
        # Show dialog
        dialog.open(parent_window, None, on_dialog_response)
    
    app.connect("activate", on_activate)
    app.run([])

if __name__ == "__main__":
    print("Testing GTK 4 FileDialog with filters...")
    test_file_dialog_filters()