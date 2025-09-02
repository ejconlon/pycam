#!/usr/bin/env python3
"""
Test script to verify that the GtkNotebook sizing fix works correctly.
This should not produce the GtkGizmo tabs negative width warning.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import sys

class TestNotebook:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("GTK4 Notebook Sizing Test")
        self.window.set_default_size(600, 400)
        
        # Create a main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        
        # Create a test notebook with width-request (the fix)
        self.notebook = Gtk.Notebook()
        self.notebook.set_vexpand(True)
        self.notebook.set_hexpand(True)
        # This is the key fix - setting a minimum width prevents negative size calculations
        self.notebook.set_size_request(200, -1)
        
        # Add some test pages
        for i in range(3):
            page_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            page_content.set_margin_top(10)
            page_content.set_margin_bottom(10)
            page_content.set_margin_start(10)
            page_content.set_margin_end(10)
            
            label = Gtk.Label(label=f"This is page {i+1}")
            page_content.append(label)
            
            button = Gtk.Button(label=f"Button {i+1}")
            page_content.append(button)
            
            # Add the page to the notebook
            tab_label = Gtk.Label(label=f"Tab {i+1}")
            self.notebook.append_page(page_content, tab_label)
        
        main_box.append(self.notebook)
        
        # Add control buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        add_button = Gtk.Button(label="Add Tab")
        add_button.connect("clicked", self.on_add_tab)
        button_box.append(add_button)
        
        remove_button = Gtk.Button(label="Remove Tab")  
        remove_button.connect("clicked", self.on_remove_tab)
        button_box.append(remove_button)
        
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit_clicked)
        button_box.append(quit_button)
        
        main_box.append(button_box)
        
        self.window.set_child(main_box)
        self.window.connect("close-request", self.on_quit_clicked)
        
        self.tab_counter = 4
        
    def on_add_tab(self, button):
        print(f"Adding tab {self.tab_counter}...")
        
        page_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        page_content.set_margin_top(10)
        page_content.set_margin_bottom(10)
        page_content.set_margin_start(10)
        page_content.set_margin_end(10)
        
        label = Gtk.Label(label=f"This is page {self.tab_counter}")
        page_content.append(label)
        
        tab_label = Gtk.Label(label=f"Tab {self.tab_counter}")
        self.notebook.append_page(page_content, tab_label)
        
        self.tab_counter += 1
        
    def on_remove_tab(self, button):
        if self.notebook.get_n_pages() > 0:
            page_num = self.notebook.get_n_pages() - 1
            print(f"Removing tab {page_num + 1}...")
            self.notebook.remove_page(page_num)
        
    def on_quit_clicked(self, *args):
        print("Quitting...")
        self.window.get_application().quit()
        return True

def main():
    app = Gtk.Application(application_id="com.example.notebooktest")
    app.connect("activate", on_activate)
    
    def timeout_quit():
        print("Auto-quitting after 5 seconds...")
        app.quit()
        return False
    
    # Auto-quit after 5 seconds to avoid hanging
    GLib.timeout_add_seconds(5, timeout_quit)
    
    return app.run(sys.argv)

def on_activate(app):
    test_notebook = TestNotebook()
    test_notebook.window.set_application(app)
    test_notebook.window.present()
    
    # Test adding/removing tabs automatically
    def auto_test():
        print("Auto-testing notebook functionality...")
        test_notebook.on_add_tab(None)
        GLib.timeout_add(500, lambda: test_notebook.on_remove_tab(None))
        GLib.timeout_add(1000, lambda: test_notebook.on_remove_tab(None))
        return False
    
    GLib.timeout_add(1500, auto_test)

if __name__ == "__main__":
    sys.exit(main())