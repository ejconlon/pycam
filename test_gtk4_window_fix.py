#!/usr/bin/env python3
"""
Test script to verify that the GTK 4 window positioning fix works correctly.
This should not produce the gdk_surface_thaw_updates error.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
import sys

class TestWindow:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("GTK4 Window Position Test")
        self.window.set_default_size(400, 300)
        
        # Create a simple layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        label = Gtk.Label(label="Testing GTK 4 window positioning fix")
        box.append(label)
        
        # Test show/hide functionality that was causing the issue
        show_button = Gtk.Button(label="Show Window")
        show_button.connect("clicked", self.on_show_clicked)
        box.append(show_button)
        
        hide_button = Gtk.Button(label="Hide Window")
        hide_button.connect("clicked", self.on_hide_clicked)
        box.append(hide_button)
        
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit_clicked)
        box.append(quit_button)
        
        self.window.set_child(box)
        self.window.connect("close-request", self.on_quit_clicked)
        
        # Create a second test window
        self.test_window = Gtk.Window()
        self.test_window.set_title("Test Dialog Window")
        self.test_window.set_default_size(300, 200)
        self.test_window.set_transient_for(self.window)
        
        test_label = Gtk.Label(label="This is a test dialog window")
        test_label.set_margin_top(20)
        test_label.set_margin_bottom(20)
        test_label.set_margin_start(20)
        test_label.set_margin_end(20)
        self.test_window.set_child(test_label)
        
    def on_show_clicked(self, button):
        print("Showing test window...")
        # This simulates the fixed show() method from the plugins
        # GTK 4: Window positioning is handled by the compositor
        # The move() method has been removed, so we skip position restoration
        self.test_window.show()
        
    def on_hide_clicked(self, button):
        print("Hiding test window...")
        # This simulates the fixed hide() method from the plugins
        # GTK 4: get_position() has been removed as windows are managed by compositor
        # We no longer store/restore position manually
        self.test_window.hide()
        
    def on_quit_clicked(self, *args):
        print("Quitting...")
        self.window.get_application().quit()
        return True

def main():
    app = Gtk.Application(application_id="com.example.gtk4windowtest")
    app.connect("activate", on_activate)
    
    def timeout_quit():
        print("Auto-quitting after 3 seconds...")
        app.quit()
        return False
    
    # Auto-quit after 3 seconds to avoid hanging
    GLib.timeout_add_seconds(3, timeout_quit)
    
    return app.run(sys.argv)

def on_activate(app):
    test_window = TestWindow()
    test_window.window.set_application(app)
    test_window.window.present()
    
    # Test the show/hide functionality automatically
    def auto_test():
        print("Auto-testing show/hide functionality...")
        test_window.on_show_clicked(None)
        GLib.timeout_add(500, lambda: test_window.on_hide_clicked(None))
        return False
    
    GLib.timeout_add(1000, auto_test)

if __name__ == "__main__":
    sys.exit(main())