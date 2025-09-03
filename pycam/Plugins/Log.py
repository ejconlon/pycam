"""
Copyright 2011 Lars Kruse <devel@sumpfralle.de>

This file is part of PyCAM.

PyCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCAM.  If not, see <http://www.gnu.org/licenses/>.
"""


import datetime
import os
import re

import pycam.Plugins
import pycam.Utils


class Log(pycam.Plugins.PluginBase):

    UI_FILE = "log.ui"
    DEPENDS = ["Clipboard"]
    CATEGORIES = ["System"]

    def setup(self):
        if not self._gtk:
            return False
        if self.gui:
            # menu item and shortcut
            # GTK 4: We don't need a UI widget for the menu action
            # The menu system will call toggle_log_window directly
            self._gtk_handlers = []
            
            # Store a flag for window visibility
            self.log_window_visible = False
            # status bar
            try:
                self.status_bar = self.gui.get_object("StatusBar")
            except:
                self.status_bar = None
                print("DEBUG: StatusBar not found in UI")
            
            try:
                event_bar = self.gui.get_object("StatusBarEventBox")
            except:
                event_bar = None
                print("DEBUG: StatusBarEventBox not found in UI")
            # GTK 4: Use GestureClick instead of button-pressed event
            if event_bar:
                click_gesture = self._gtk.GestureClick.new()
                click_gesture.connect("pressed", lambda gesture, n_press, x, y: self.toggle_log_window())
                event_bar.add_controller(click_gesture)
                event_bar.unparent()
                self.core.register_ui("main_window", "Status", event_bar, 100)
            # "log" window
            try:
                self.log_window = self.gui.get_object("LogWindow")
                self.log_window.set_default_size(500, 400)
                hide_window = lambda *args: self.toggle_log_window(value=False)
                self._gtk_handlers.extend([
                    (self.log_window, "close-request", hide_window),
                    (self.log_window, "destroy", hide_window)])
                
                # Try to get buttons, but don't fail if they don't exist
                try:
                    close_button = self.gui.get_object("LogWindowClose")
                    self._gtk_handlers.append((close_button, "clicked", hide_window))
                except:
                    pass
                    
                try:
                    clear_button = self.gui.get_object("LogWindowClear")
                    self._gtk_handlers.append((clear_button, "clicked", self.clear_log_window))
                except:
                    pass
                    
                try:
                    copy_button = self.gui.get_object("LogWindowCopyToClipboard")
                    self._gtk_handlers.append((copy_button, "clicked", self.copy_log_to_clipboard))
                except:
                    pass
            except Exception as e:
                print(f"DEBUG: LogWindow not found, will create one when needed: {e}")
                self.log_window = None
            try:
                self.log_model = self.gui.get_object("LogWindowList")
            except:
                print("DEBUG: LogWindowList not found, creating new ListStore")
                # Create a new ListStore with timestamp, type, and message columns
                self.log_model = self._gtk.ListStore(str, str, str)
            # window state
            self._log_window_position = None
            # register a callback for the log window
            pycam.Utils.log.add_hook(self.add_log_message)
            self.register_gtk_handlers(self._gtk_handlers)
        return True

    def teardown(self):
        if self.gui:
            self.unregister_gtk_handlers(self._gtk_handlers)
            if self.log_window:
                self.log_window.hide()
            # Clean up any registered UI elements
            try:
                event_bar = self.gui.get_object("StatusBarEventBox")
                if event_bar:
                    self.core.unregister_ui("main_window", event_bar)
            except:
                pass
            # TODO: disconnect the log handler

    def add_log_message(self, title, message, record=None):
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime("%H:%M")
        # avoid the ugly character for a linefeed
        message = " ".join(message.splitlines())
        if self.log_model:
            self.log_model.append((timestamp, title, message))
        # update the status bar (if the GTK interface is still active)
        if self.status_bar and self.status_bar.get_parent() is not None:
            # remove the last message from the stack (probably not necessary)
            self.status_bar.pop(0)
            # push the new message
            try:
                self.status_bar.push(0, message)
            except TypeError:
                new_message = re.sub(r"[^\w\s]", "", message)
                self.status_bar.push(0, new_message)
            # highlight the "warning" icon for warnings/errors
            if record and record.levelno > 20:
                self.gui.get_object("StatusBarWarning").show()

    def copy_log_to_clipboard(self, widget=None):
        def copy_row(model, path, it, content):
            columns = []
            for column in range(model.get_n_columns()):
                columns.append(model.get_value(it, column))
            content.append(" ".join(columns))
        content = []
        self.log_model.foreach(copy_row, content)
        self.core.get("clipboard-set")(os.linesep.join(content))
        self.gui.get_object("StatusBarWarning").hide()

    def clear_log_window(self, widget=None):
        if self.log_model:
            self.log_model.clear()
        try:
            warning = self.gui.get_object("StatusBarWarning")
            if warning:
                warning.hide()
        except:
            pass

    def toggle_log_window(self, widget=None, value=None, action=None):
        # GTK 4: Simplified toggle without checkbox dependency
        if value is not None:
            new_state = value
        else:
            # Toggle current state
            new_state = not getattr(self, 'log_window_visible', False)
        
        self.log_window_visible = new_state
        
        if self.log_window:
            if new_state:
                self.log_window.show()
            else:
                self.log_window.hide()
        
        # Hide warning icon if we have status bar
        try:
            warning_icon = self.gui.get_object("StatusBarWarning")
            if warning_icon:
                warning_icon.hide()
        except:
            pass
        # don't destroy the window with a "destroy" event
        return True
