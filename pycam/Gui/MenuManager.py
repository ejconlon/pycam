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
        
        # Export submenu (placeholder for now)
        export_menu = Gio.Menu()
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
        # Placeholder - will be populated by plugins
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
            
            # App-wide actions
            ("quit", self.callback_handler.destroy, "<Control>q"),
        ]
        
        for action_name, callback, accelerator in actions:
            if callback:
                action = Gio.SimpleAction.new(action_name, None)
                action.connect("activate", lambda action, param, cb=callback: cb())
                self.action_group.add_action(action)
                
                # Add keyboard accelerator if specified
                if accelerator and self.application:
                    self.application.set_accels_for_action(f"app.{action_name}", [accelerator])
    
    def get_action_group(self):
        """Get the action group for adding to windows"""
        return self.action_group