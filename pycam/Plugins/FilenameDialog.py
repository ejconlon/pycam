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
    # Mime type mappings for common CAD/CAM formats
    mime_types = {
        "*.stl": ["model/stl", "application/sla"],
        "*.dxf": ["image/vnd.dxf", "application/dxf"], 
        "*.svg": ["image/svg+xml"],
        "*.eps": ["application/postscript"],
        "*.ps": ["application/postscript"]
    }
    
    for one_filter in filter_list:
        current_filter = gtk.FileFilter()
        current_filter.set_name(one_filter[0])
        file_extensions = one_filter[1]
        if not isinstance(file_extensions, (list, tuple)):
            file_extensions = [file_extensions]
        for ext in file_extensions:
            # GTK 4: Add multiple patterns for better compatibility
            # Basic pattern
            current_filter.add_pattern(ext)
            # Uppercase version
            current_filter.add_pattern(ext.upper())
            # Lowercase version  
            current_filter.add_pattern(ext.lower())
            # Case insensitive pattern (for compatibility)
            case_insensitive_pattern = pycam.Utils.get_case_insensitive_file_pattern(ext)
            current_filter.add_pattern(case_insensitive_pattern)
            
            # GTK 4: Add mime types if known (helps with file filtering)
            if ext in mime_types:
                for mime_type in mime_types[ext]:
                    current_filter.add_mime_type(mime_type)
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
    filter_ext = filter_ext[1:]
    if filter_ext and not filename.endswith(filter_ext):
        return filename + filter_ext
    else:
        return filename


class FilenameDialog(pycam.Plugins.PluginBase):

    CATEGORIES = ["System"]

    def setup(self):
        # FilenameDialog works with or without a GUI builder object
        # since we create dialogs programmatically
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
        
        from gi.repository import Gio, GLib
        
        try:
            # GTK 4.10+: Use the modern FileDialog API
            dialog = self._gtk.FileDialog()
            dialog.set_title(title)
        except Exception as e:
            print(f"Error creating FileDialog: {e}")
            return None
        
        # Set initial folder
        if self.last_dirname and os.path.isdir(self.last_dirname):
            try:
                folder = Gio.File.new_for_path(self.last_dirname)
                dialog.set_initial_folder(folder)
            except Exception as e:
                print(f"Error setting initial folder: {e}")
        
        # Build filters using the new ListStore model
        if type_filter:
            try:
                filter_store = Gio.ListStore.new(self._gtk.FileFilter)
                
                # Add specific filters first
                for file_filter in _get_filters_from_list(self._gtk, type_filter):
                    filter_store.append(file_filter)
                
                # Add "All files" filter last
                all_filter = self._gtk.FileFilter()
                all_filter.set_name("All files")
                all_filter.add_pattern("*")
                filter_store.append(all_filter)
                
                # Set the filters on the dialog
                dialog.set_filters(filter_store)
                
                # Set the first specific filter as default (not "All files")
                if filter_store.get_n_items() > 0:
                    dialog.set_default_filter(filter_store.get_item(0))
                    
            except Exception as e:
                print(f"Error setting up file filters: {e}")
                # Continue without filters if there's an error
        
        # Handle filename templates for save mode
        if not mode_load and filename_templates:
            valid_templates = []
            for template in filename_templates:
                if template:
                    if hasattr(template, "get_path"):
                        valid_templates.append(template.get_path())
                    else:
                        valid_templates.append(template)
            if valid_templates:
                filename_template = valid_templates[0]
                default_filename = os.path.splitext(filename_template)[0]
                if filename_extension:
                    default_filename += os.path.extsep + filename_extension
                dialog.set_initial_name(os.path.basename(default_filename))
        
        # Show dialog and wait for response (synchronous for compatibility)
        filename = None
        loop = GLib.MainLoop()
        
        def on_finish(dialog, result):
            nonlocal filename
            try:
                if mode_load:
                    file = dialog.open_finish(result)
                else:
                    file = dialog.save_finish(result)
                if file:
                    filename = file.get_path()
            except GLib.Error as e:
                print(f"Dialog operation cancelled or error: {e}")
            except Exception as e:
                print(f"Unexpected dialog error: {e}")
            finally:
                loop.quit()
        
        try:
            # Ensure parent window is valid
            if parent is None:
                print("Warning: No parent window available for dialog")
            
            if mode_load:
                dialog.open(parent, None, on_finish)
            else:
                dialog.save(parent, None, on_finish)
            
            loop.run()
        except Exception as e:
            print(f"Error showing dialog: {e}")
            return None
        
        if filename:
            self.last_dirname = os.path.dirname(filename)
            
            if not mode_load and filename:
                # check if we want to add a default suffix
                filename = _get_filename_with_suffix(filename, type_filter)
                
            if not mode_load and os.path.exists(filename):
                # Simple confirmation for overwrite
                import sys
                response = input(f"File '{filename}' exists. Overwrite? (y/N): ").strip().lower()
                if response not in ['y', 'yes']:
                    return None
        
        return filename