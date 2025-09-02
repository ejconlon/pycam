#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class TestWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("PyCAM GTK 4 Test")
        self.set_default_size(400, 300)
        
        # Create a simple layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        label = Gtk.Label(label="PyCAM GTK 4 Test")
        box.append(label)
        
        button = Gtk.Button(label="Click me!")
        button.connect("clicked", self.on_button_clicked)
        box.append(button)
        
        self.set_child(box)
    
    def on_button_clicked(self, button):
        print("Button clicked! GTK 4 is working!")

class TestApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.pycam.test")
    
    def do_activate(self):
        win = TestWindow(self)
        win.present()

def main():
    app = TestApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    main()