#!/usr/bin/env python3
"""
GTK 4 Menu System for PyCAM

This replaces the old GtkAction/UIManager system with GTK 4's GMenu/GSimpleAction approach.
"""

from gi.repository import Gio, GLib


class MenuManager:
    """Manages the application menu system for GTK 4"""
    
    def __init__(self, application, callback_handler):
        self.application = application
        self.callback_handler = callback_handler
        self.action_group = Gio.SimpleActionGroup()
        self.menubar = None
        
    def create_menubar(self):
        """Create the main menubar using GMenu"""
        # First create all the actions
        self.create_actions()
        
        self.menubar = Gio.Menu()
        
        # Create main menu sections
        file_menu = self._create_file_menu()
        edit_menu = self._create_edit_menu()
        settings_menu = self._create_settings_menu()
        view_menu = self._create_view_menu()
        help_menu = self._create_help_menu()
        
        # Add menus to menubar
        self.menubar.append_submenu("_File", file_menu)
        self.menubar.append_submenu("_Edit", edit_menu)
        self.menubar.append_submenu("_Settings", settings_menu)
        self.menubar.append_submenu("_View", view_menu)
        self.menubar.append_submenu("_Help", help_menu)
        
        return self.menubar
    
    def _create_file_menu(self):
        """Create File menu"""
        menu = Gio.Menu()
        
        # File operations
        menu.append("_Open Model...", "app.open-model")
        menu.append("Open _Recent", "app.open-recent")
        
        # Export submenu
        export_menu = Gio.Menu()
        export_menu.append("Export _G-Code...", "app.export-gcode")
        export_menu.append("Export _STL Model...", "app.export-stl") 
        export_menu.append("Export Tool_path...", "app.export-toolpath")
        menu.append_submenu("_Export", export_menu)
        
        return menu
    
    def _create_edit_menu(self):
        """Create Edit menu"""
        menu = Gio.Menu()
        menu.append("_Undo", "app.undo")
        return menu
    
    def _create_settings_menu(self):
        """Create Settings menu"""
        menu = Gio.Menu()
        
        menu.append("Reset Workspace to Defaults", "app.reset-workspace")
        menu.append("_Load Workspace...", "app.load-workspace")
        menu.append("_Save Workspace", "app.save-workspace")
        menu.append("Save Workspace _as...", "app.save-workspace-as")
        menu.append("_Preferences", "app.preferences")
        
        return menu
    
    def _create_view_menu(self):
        """Create View menu"""
        menu = Gio.Menu()
        
        # Add essential view menu items that users expect
        menu.append("Toggle _Log Window", "app.toggle-log")
        menu.append("Toggle _Memory Analyzer", "app.toggle-memory")
        menu.append("Toggle _Plugin Selector", "app.toggle-plugins")
        menu.append("Toggle _Console", "app.toggle-console")
        
        # Separator
        menu.append_section(None, Gio.Menu())
        
        # 3D View options
        menu.append("Reset 3D _View", "app.reset-3d-view")
        
        return menu
    
    def _create_help_menu(self):
        """Create Help menu"""
        menu = Gio.Menu()
        
        # Help documentation
        menu.append("User _Manual: Overview", "app.help-manual")
        menu.append("_Introduction", "app.help-intro")
        
        # Help submenus
        misc_menu = self._create_help_misc_menu()
        gui_menu = self._create_help_gui_menu()
        
        menu.append_submenu("Mis_cellaneous", misc_menu)
        menu.append_submenu("_GUI description", gui_menu)
        
        # External links
        menu.append("Project _Website", "app.help-website")
        menu.append("_Forum", "app.help-forum")
        menu.append("Re_quest a Feature", "app.help-feature-request")
        menu.append("Report a _Bug", "app.help-bug-tracker")
        menu.append("_Development Blog", "app.help-blog")
        
        menu.append("_About", "app.about")
        
        return menu
    
    def _create_help_misc_menu(self):
        """Create Help > Miscellaneous submenu"""
        menu = Gio.Menu()
        
        menu.append("Supported _Formats", "app.help-formats")
        menu.append("_Model Transformations", "app.help-transforms")
        menu.append("_GCode Export", "app.help-gcode")
        menu.append("_Simulation", "app.help-simulation")
        menu.append("Server Mode", "app.help-server")
        menu.append("_Command Line Usage", "app.help-cli")
        menu.append("_Keyboard Shortcuts", "app.help-hotkeys")
        menu.append("_Touch off and tool change", "app.help-touchoff")
        
        return menu
    
    def _create_help_gui_menu(self):
        """Create Help > GUI description submenu"""
        menu = Gio.Menu()
        
        menu.append("T_ool Types", "app.help-tools")
        menu.append("_Process Settings", "app.help-process")
        menu.append("_Bounds Settings", "app.help-bounds")
        menu.append("_Project Setup", "app.help-project")
        menu.append("3D _View", "app.help-3dview")
        
        return menu
    
    def create_actions(self):
        """Create all GSimpleActions for menu items"""
        print("🔥 CREATING MENU ACTIONS! 🔥")
        actions = [
            # File menu
            ("open-model", self.callback_handler.load_model_file, "<Control>o"),
            ("open-recent", None, None),
            
            # Edit menu
            ("undo", self.callback_handler.restore_undo_state, "<Control>z"),
            
            # Settings menu
            ("reset-workspace", None, None),
            ("load-workspace", None, None),
            ("save-workspace", None, None),
            ("save-workspace-as", None, None),
            ("preferences", self.callback_handler.toggle_preferences_window, "<Control>p"),
            
            # Help menu - documentation
            ("help-manual", lambda *args: self.callback_handler.show_help("user-manual"), "F1"),
            ("help-intro", lambda *args: self.callback_handler.show_help("introduction"), None),
            ("help-formats", lambda *args: self.callback_handler.show_help("supported-formats"), None),
            ("help-transforms", lambda *args: self.callback_handler.show_help("model-transformations"), None),
            ("help-gcode", lambda *args: self.callback_handler.show_help("gcode-export"), None),
            ("help-simulation", lambda *args: self.callback_handler.show_help("simulation"), None),
            ("help-server", lambda *args: self.callback_handler.show_help("server-mode"), None),
            ("help-cli", lambda *args: self.callback_handler.show_help("cli-examples"), None),
            ("help-hotkeys", lambda *args: self.callback_handler.show_help("keyboard-shortcuts"), None),
            ("help-touchoff", lambda *args: self.callback_handler.show_help("touch-off"), None),
            ("help-tools", lambda *args: self.callback_handler.show_help("tool-types"), None),
            ("help-process", lambda *args: self.callback_handler.show_help("process-settings"), None),
            ("help-bounds", lambda *args: self.callback_handler.show_help("bounding-box"), None),
            ("help-project", lambda *args: self.callback_handler.show_help("project-setup"), None),
            ("help-3dview", lambda *args: self.callback_handler.show_help("3d-view"), None),
            
            # Help menu - external links
            ("help-website", lambda *args: self.callback_handler.show_help("http://pycam.sourceforge.net"), None),
            ("help-forum", lambda *args: self.callback_handler.show_help("http://sourceforge.net/projects/pycam/forums"), None),
            ("help-feature-request", lambda *args: self.callback_handler.show_help("https://github.com/SebKuzminsky/pycam/issues/"), None),
            ("help-bug-tracker", lambda *args: self.callback_handler.show_help("https://github.com/SebKuzminsky/pycam/issues/"), None),
            ("help-blog", lambda *args: self.callback_handler.show_help("http://fab.senselab.org/pycam"), None),
            
            # About
            ("about", lambda *args: self.callback_handler.toggle_about_window(True), None),
            
            # Export actions
            ("export-gcode", self._export_gcode, None),
            ("export-stl", self._export_stl, None),
            ("export-toolpath", self._export_toolpath, None),
            
            # View menu actions
            ("toggle-log", self._toggle_log_window, None),
            ("toggle-memory", self._toggle_memory_window, None), 
            ("toggle-plugins", self._toggle_plugins_window, None),
            ("toggle-console", self._toggle_console_window, None),
            ("reset-3d-view", self._reset_3d_view, None),
            
            # App-wide actions
            ("quit", self.callback_handler.destroy, "<Control>q"),
        ]
        
        for action_name, callback, accelerator in actions:
            if callback:
                action = Gio.SimpleAction.new(action_name, None)
                action.connect("activate", lambda action, param, cb=callback: cb())
                self.action_group.add_action(action)
                print(f"DEBUG: Created action '{action_name}' with callback {callback}")
                
                # Add keyboard accelerator if specified
                if accelerator and self.application:
                    self.application.set_accels_for_action(f"app.{action_name}", [accelerator])
    
    def get_action_group(self):
        """Get the action group for adding to windows"""
        return self.action_group
    
    def populate_dynamic_menus(self, core):
        """Populate View and Export menus from registered UI items"""
        try:
            print(f"DEBUG: populate_dynamic_menus called with core: {core}")
            
            # Debug loaded plugins
            if hasattr(core, '_plugins'):
                plugins = core._plugins
                print(f"DEBUG: Found {len(plugins)} loaded plugins:")
                for name, plugin in plugins.items():
                    print(f"DEBUG: - {name}: {type(plugin).__name__}")
                    if hasattr(plugin, 'toggle_window'):
                        print(f"DEBUG:   + has toggle_window method")
                    if hasattr(plugin, 'toggle_log_window'):
                        print(f"DEBUG:   + has toggle_log_window method")
                    if hasattr(plugin, 'toggle_console_window'):
                        print(f"DEBUG:   + has toggle_console_window method")
            else:
                print("DEBUG: core has no _plugins attribute")
                
            if hasattr(core, 'ui_sections'):
                print(f"DEBUG: ui_sections available: {list(core.ui_sections.keys())}")
                if 'view_menu' in core.ui_sections:
                    section = core.ui_sections['view_menu']
                    print(f"DEBUG: view_menu has {len(section.widgets)} widgets:")
                    for w in section.widgets:
                        print(f"DEBUG: - {w.name}: {type(w.obj)} (weight: {w.weight})")
                else:
                    print("DEBUG: view_menu not found in ui_sections")
            else:
                print("DEBUG: core has no ui_sections attribute")
                
            self._populate_view_menu(core)
            self._populate_export_menu(core)
        except Exception as e:
            print(f"DEBUG: Error populating dynamic menus: {e}")
            import traceback
            traceback.print_exc()
    
    def _populate_view_menu(self, core):
        """Populate View menu from view_menu UI registrations"""
        try:
            # Get registered view_menu items from core
            if hasattr(core, 'ui_sections') and 'view_menu' in core.ui_sections:
                view_section = core.ui_sections['view_menu']
                # Sort by weight (priority)
                sorted_widgets = sorted(view_section.widgets, key=lambda x: x.weight)
                
                # Find the View submenu in our menubar
                view_submenu = None
                for i in range(self.menubar.get_n_items()):
                    item_link = self.menubar.get_item_link(i, "submenu")
                    if item_link and "View" in str(item_link):
                        # Get the submenu
                        view_submenu = self.menubar.get_item_attribute_value(i, "submenu", None)
                        break
                
                # Add registered items to View menu
                for widget_info in sorted_widgets:
                    if hasattr(widget_info.obj, 'get_label'):
                        label = widget_info.obj.get_label() or widget_info.name
                    else:
                        label = widget_info.name
                    
                    # Create action for this menu item
                    action_name = f"view-{widget_info.name.lower().replace(' ', '-')}"
                    
                    # Try to connect to widget's activate signal
                    if hasattr(widget_info.obj, 'get_active') and hasattr(widget_info.obj, 'set_active'):
                        # Toggle action for checkable items
                        action = Gio.SimpleAction.new_stateful(
                            action_name, None, GLib.Variant.new_boolean(False))
                        action.connect("activate", self._create_toggle_callback(widget_info.obj))
                    else:
                        # Regular action
                        action = Gio.SimpleAction.new(action_name, None)
                        if hasattr(widget_info.obj, 'clicked'):
                            action.connect("activate", lambda a, p, obj=widget_info.obj: obj.emit('clicked'))
                    
                    self.action_group.add_action(action)
                    
                    print(f"DEBUG: Added view menu item: {label} -> app.{action_name}")
                    
        except Exception as e:
            print(f"DEBUG: Error populating view menu: {e}")
    
    def _populate_export_menu(self, core):
        """Populate Export menu from export-related UI registrations"""  
        try:
            # Add some basic export options
            export_submenu = None
            
            # Find File menu and its Export submenu
            for i in range(self.menubar.get_n_items()):
                # This is a simplified approach - we'd need to traverse the menu structure properly
                pass
                
            print("DEBUG: Export menu population not fully implemented yet")
            
        except Exception as e:
            print(f"DEBUG: Error populating export menu: {e}")
    
    def _create_toggle_callback(self, widget):
        """Create a callback for toggle menu items"""
        def callback(action, parameter):
            try:
                current_state = action.get_state().get_boolean()
                new_state = not current_state
                action.set_state(GLib.Variant.new_boolean(new_state))
                widget.set_active(new_state)
            except Exception as e:
                print(f"DEBUG: Toggle callback error: {e}")
        return callback
    
    def _test_action(self, *args):
        """Test action to see if menu system works at all"""
        print("🎉🎉🎉 TEST ACTION TRIGGERED! MENU SYSTEM WORKS! 🎉🎉🎉")
        import subprocess
        subprocess.run(['say', 'Menu action triggered'], check=False)
    
    def _reset_3d_view(self, *args):
        """Reset the 3D view to default position"""
        try:
            # Try to access the OpenGL view through registered UI widgets
            if hasattr(self.callback_handler, 'settings'):
                core = self.callback_handler.settings
                if hasattr(core, 'ui_sections') and 'view_menu' in core.ui_sections:
                    ui_section = core.ui_sections['view_menu']
                    # Look for ViewOpenGL widget
                    for widget_info in ui_section.widgets:
                        if widget_info.name == 'ViewOpenGL':
                            # Found the OpenGL view toggle - we can try to reset it
                            if hasattr(widget_info.obj, 'emit'):
                                # Toggle it off and on to reset
                                widget_info.obj.set_active(False)
                                widget_info.obj.set_active(True)
                            return
                
                # Fallback: try to find the integrated GLArea directly
                if hasattr(self.callback_handler, 'gl_area'):
                    self.callback_handler.gl_area.queue_render()
                    
        except Exception as e:
            print(f"DEBUG: Reset 3D view error: {e}")
    
    # View menu action implementations
    def _toggle_log_window(self, *args):
        """Toggle the log window"""
        print("🔥 LOG MENU CLICKED! 🔥")
        try:
            # Try to find and use the Log plugin
            # The callback_handler is ProjectGui, which has settings (the event_manager)
            if hasattr(self.callback_handler, 'settings'):
                core = self.callback_handler.settings
                
                # Try to get plugins from plugin manager
                plugin_manager = core.get("plugin_manager")
                if plugin_manager:
                    plugins = plugin_manager.modules
                    print(f"DEBUG: Found {len(plugins)} plugins from plugin_manager: {list(plugins.keys())}")
                else:
                    # Fallback to _plugins attribute
                    plugins = getattr(core, '_plugins', {})
                    print(f"DEBUG: Found {len(plugins)} plugins from _plugins: {list(plugins.keys())}")
                
                # Look for Log plugin specifically
                if 'Log' in plugins:
                    log_plugin = plugins['Log']
                    print(f"DEBUG: Found Log plugin directly: {log_plugin}")
                    if hasattr(log_plugin, 'toggle_log_window'):
                        print(f"DEBUG: Calling toggle_log_window on Log plugin")
                        log_plugin.toggle_log_window()
                        return
                
                # Look for loaded plugins
                for name, plugin_instance in plugins.items():
                    print(f"DEBUG: Checking plugin {name}: {type(plugin_instance).__name__}")
                    if hasattr(plugin_instance, 'toggle_log_window'):
                        print(f"DEBUG: Found Log plugin, calling toggle_log_window")
                        plugin_instance.toggle_log_window()
                        return
                
            # If no plugin found, create a simple log window
            print("DEBUG: No Log plugin found, creating simple window")
            from gi.repository import Gtk
            window = Gtk.Window(title="Log Window")
            window.set_default_size(500, 400)
            
            # Add a simple text view
            scrolled = Gtk.ScrolledWindow()
            text_view = Gtk.TextView()
            text_view.set_editable(False)
            text_view.get_buffer().set_text("Log window placeholder\n\nThe Log plugin is not loaded.\nThis is a placeholder window.")
            scrolled.set_child(text_view)
            window.set_child(scrolled)
            
            window.show()
            print("DEBUG: Simple log window shown")
            
        except Exception as e:
            print(f"DEBUG: Toggle log window error: {e}")
            import traceback
            traceback.print_exc()
    
    def _toggle_memory_window(self, *args):
        """Toggle the memory analyzer window"""
        print("🔥 MEMORY MENU CLICKED! 🔥")
        try:
            # Try to find and use the MemoryAnalyzer plugin
            if hasattr(self.callback_handler, 'settings'):
                core = self.callback_handler.settings
                
                # Try to get plugins from plugin manager
                plugin_manager = core.get("plugin_manager")
                if plugin_manager:
                    plugins = plugin_manager.modules
                    print(f"DEBUG: Found {len(plugins)} plugins from plugin_manager: {list(plugins.keys())}")
                else:
                    plugins = getattr(core, '_plugins', {})
                    print(f"DEBUG: Found {len(plugins)} plugins from _plugins: {list(plugins.keys())}")
                
                # Look for loaded plugins
                for name, plugin_instance in plugins.items():
                    if hasattr(plugin_instance, 'toggle_window') and type(plugin_instance).__name__ == 'MemoryAnalyzer':
                        print(f"DEBUG: Found MemoryAnalyzer plugin, calling toggle_window")
                        plugin_instance.toggle_window()
                        return
            
            # If no plugin found, create a simple memory window
            print("DEBUG: No MemoryAnalyzer plugin found, creating simple window")
            from gi.repository import Gtk
            window = Gtk.Window(title="Memory Analyzer")
            window.set_default_size(500, 400)
            
            # Add a simple label
            label = Gtk.Label(label="Memory Analyzer\n\nThe MemoryAnalyzer plugin is not loaded.\nThis is a placeholder window.")
            window.set_child(label)
            
            window.show()
            print("DEBUG: Simple memory window shown")
            
        except Exception as e:
            print(f"DEBUG: Toggle memory window error: {e}")
            import traceback
            traceback.print_exc()
            
    def _toggle_plugins_window(self, *args):
        """Toggle the plugin selector window"""
        try:
            print(f"DEBUG: _toggle_plugins_window called")
            # Find the PluginSelector plugin directly and call its toggle method
            if hasattr(self.callback_handler, 'settings'):
                core = self.callback_handler.settings
                # Look for loaded plugins that have the right functionality  
                for plugin_instance in getattr(core, '_plugins', {}).values():
                    if type(plugin_instance).__name__ == 'PluginSelector':
                        print(f"DEBUG: Found PluginSelector plugin")
                        if hasattr(plugin_instance, 'toggle_window'):
                            print(f"DEBUG: Calling toggle_window")
                            plugin_instance.toggle_window()
                        elif hasattr(plugin_instance, 'toggle_plugin_window'):
                            print(f"DEBUG: Calling toggle_plugin_window")
                            plugin_instance.toggle_plugin_window()
                        return
                print("DEBUG: No PluginSelector plugin found")
            else:
                print("DEBUG: No core found in callback_handler")
        except Exception as e:
            print(f"DEBUG: Toggle plugins window error: {e}")
            import traceback
            traceback.print_exc()
    
    def _toggle_console_window(self, *args):
        """Toggle the console window"""
        try:
            print(f"DEBUG: _toggle_console_window called")
            # Find the GtkConsole plugin directly and call its toggle method
            if hasattr(self.callback_handler, 'settings'):
                core = self.callback_handler.settings
                # Look for loaded plugins that have the right functionality  
                for plugin_instance in getattr(core, '_plugins', {}).values():
                    if type(plugin_instance).__name__ == 'GtkConsole':
                        print(f"DEBUG: Found GtkConsole plugin")
                        if hasattr(plugin_instance, 'toggle_console_window'):
                            print(f"DEBUG: Calling toggle_console_window")
                            plugin_instance.toggle_console_window()
                        elif hasattr(plugin_instance, 'toggle_window'):
                            print(f"DEBUG: Calling toggle_window")
                            plugin_instance.toggle_window()
                        return
                print("DEBUG: No GtkConsole plugin found")
            else:
                print("DEBUG: No core found in callback_handler")
        except Exception as e:
            print(f"DEBUG: Toggle console window error: {e}")
            import traceback
            traceback.print_exc()
    
    # Export menu action implementations  
    def _export_gcode(self, *args):
        """Export G-code"""
        print("🔥 EXPORT G-CODE MENU CLICKED! 🔥")
        try:
            print("DEBUG: G-code export requested")
            # This would normally open a file dialog and export G-code
            # For now, just show a placeholder message
            if hasattr(self.callback_handler, 'show_help'):
                self.callback_handler.show_help(None, "gcode-export")
            else:
                print("G-code export functionality not yet implemented")
        except Exception as e:
            print(f"DEBUG: Export G-code error: {e}")
            
    def _export_stl(self, *args):
        """Export STL model"""
        try:
            print("DEBUG: STL export requested")
            print("STL export functionality not yet implemented")
        except Exception as e:
            print(f"DEBUG: Export STL error: {e}")
            
    def _export_toolpath(self, *args):
        """Export toolpath"""
        try:
            print("DEBUG: Toolpath export requested") 
            print("Toolpath export functionality not yet implemented")
        except Exception as e:
            print(f"DEBUG: Export toolpath error: {e}")