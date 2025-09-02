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

import os

import pycam.Plugins
import pycam.Utils


def _get_filters_from_list(gtk, filter_list):
    result = []
    for one_filter in filter_list:
        current_filter = gtk.FileFilter()
        current_filter.set_name(one_filter[0])
        file_extensions = one_filter[1]
        if not isinstance(file_extensions, (list, tuple)):
            file_extensions = [file_extensions]
        for ext in file_extensions:
            current_filter.add_pattern(pycam.Utils.get_case_insensitive_file_pattern(ext))
        result.append(current_filter)
    return result


def _get_filename_with_suffix(filename, type_filter):
    # use the first extension provided by the filter as the default
    if isinstance(type_filter[0], (tuple, list)):
        filter_ext = type_filter[0][1]
    else:
        filter_ext = type_filter[1]
    if isinstance(filter_ext, (list, tuple)):
        filter_ext = filter_ext[0]
    if not filter_ext.startswith("*"):
        # weird filter content
        return filename
    else:
        filter_ext = filter_ext[1:]
    basename = os.path.basename(filename)
    if (basename.rfind(".") == -1) or (basename[-6:].rfind(".") == -1):
        # The filename does not contain a dot or the dot is not within the
        # last five characters. Dots within the start of the filename are
        # ignored.
        return filename + filter_ext
    else:
        # contains at least one dot
        return filename


class FilenameDialog(pycam.Plugins.PluginBase):

    CATEGORIES = ["System"]

    def setup(self):
        if not self._gtk:
            return False
        else:
            self.last_dirname = None
            self.core.set("get_filename_func", self.get_filename_dialog)
            return True

    def teardown(self):
        self.core.set("get_filename_func", None)

    def get_filename_dialog(self, title="Choose file ...", mode_load=False, type_filter=None,
                            filename_templates=None, filename_extension=None, parent=None,
                            extra_widget=None):
        if parent is None:
            parent = self.core.get("main_window")
        
        # GTK 4: Create file dialog 
        if mode_load:
            dialog = self._gtk.FileChooserNative(
                title=title,
                transient_for=parent,
                action=self._gtk.FileChooserAction.OPEN
            )
            # GTK 4: Labels are handled automatically by FileChooserNative
        else:
            dialog = self._gtk.FileChooserNative(
                title=title,
                transient_for=parent,
                action=self._gtk.FileChooserAction.SAVE
            )
            # GTK 4: Labels are handled automatically by FileChooserNative
        # set the initial directory to the last one used  
        if self.last_dirname and os.path.isdir(self.last_dirname):
            # GTK 4: Use GFile for current folder
            from gi.repository import Gio
            folder = Gio.File.new_for_path(self.last_dirname)
            dialog.set_current_folder(folder)
        
        # GTK 4: FileChooserNative doesn't support extra widgets
        # Skip extra_widget functionality for now (rarely used)
        if extra_widget:
            # TODO: Implement alternative UI for extra widgets if needed
            pass
        # add filter for files
        if type_filter:
            for file_filter in _get_filters_from_list(self._gtk, type_filter):
                dialog.add_filter(file_filter)
        # guess the export filename based on the model's filename
        valid_templates = []
        if filename_templates:
            for template in filename_templates:
                if not template:
                    continue
                elif hasattr(template, "get_path"):
                    valid_templates.append(template.get_path())
                else:
                    valid_templates.append(template)
        if valid_templates:
            filename_template = valid_templates[0]
            # remove the extension
            default_filename = os.path.splitext(filename_template)[0]
            if filename_extension:
                default_filename += os.path.extsep + filename_extension
            elif type_filter:
                for one_type in type_filter:
                    extension = one_type[1]
                    if isinstance(extension, (list, tuple, set)):
                        extension = extension[0]
                    # use only the extension of the type filter string
                    extension = os.path.splitext(extension)[1]
                    if extension:
                        default_filename += extension
                        # finish the loop
                        break
            # GTK 4: Set initial filename 
            if mode_load:
                from gi.repository import Gio
                file = Gio.File.new_for_path(default_filename)
                dialog.set_file(file)
            else:
                dialog.set_current_name(os.path.basename(default_filename))
        # add filter for all files
        ext_filter = self._gtk.FileFilter()
        ext_filter.set_name("All files")
        ext_filter.add_pattern("*")
        dialog.add_filter(ext_filter)
        # GTK 4: For FileChooserNative, we need to handle it synchronously
        # Store the result
        filename = None
        
        def response_callback(dialog, response_id):
            nonlocal filename
            if response_id == self._gtk.ResponseType.ACCEPT:
                selected_file = dialog.get_file()
                if selected_file:
                    filename = selected_file.get_path()
            # Quit the local main loop
            loop.quit()
        
        # Connect the response signal
        dialog.connect('response', response_callback)
        
        # Create a local main loop
        from gi.repository import GLib
        loop = GLib.MainLoop()
        
        # Show the dialog
        dialog.show()
        
        # Run the local main loop (this blocks until dialog is closed)
        loop.run()
        
        # Clean up
        dialog.destroy()
        
        if not filename:
            return None
            
        uri = pycam.Utils.URIHandler(filename)
        
        if not mode_load and filename:
            # check if we want to add a default suffix
            filename = _get_filename_with_suffix(filename, type_filter)
            
        if not mode_load and os.path.exists(filename):
            # GTK 4: Simple confirmation for overwrite (synchronous)
            # TODO: Use proper async AlertDialog when we have better async support
            import sys
            response = input(f"File '{filename}' exists. Overwrite? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                return None
            
        elif mode_load and not uri.exists():
            print(f"Error: File '{filename}' does not exist.")
            return None
            
        # add the file to the list of recently used ones
        if filename:
            self.core.get("set_last_filename")(filename)
            # Update last directory for next dialog
            self.last_dirname = os.path.dirname(filename)
            
        return filename
