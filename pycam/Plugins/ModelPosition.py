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


import pycam.Plugins


class ModelPosition(pycam.Plugins.PluginBase):

    UI_FILE = "model_position.ui"
    DEPENDS = ["Models"]
    CATEGORIES = ["Model"]

    def setup(self):
        if self.gui:
            position_box = self.gui.get_object("ModelPositionBox")
            position_box.unparent()
            self._gtk_handlers = []
            self.core.register_ui("model_handling", "Position", position_box, -20)
            shift_button = self.gui.get_object("ShiftModelButton")
            self._gtk_handlers.append((shift_button, "clicked", self._shift_model))
            align_button = self.gui.get_object("AlignPositionButton")
            self._gtk_handlers.append((align_button, "clicked", self._align_model))
            # GTK 4: Use EventControllerFocus instead of focus-in/focus-out signals
            # grab default button for shift/align controls
            for axis in "XYZ":
                obj = self.gui.get_object("ShiftPosition%s" % axis)
                focus_controller = self._gtk.EventControllerFocus.new()
                focus_controller.connect("enter", lambda controller: shift_button.grab_default())
                focus_controller.connect("leave", lambda controller: 
                    shift_button.get_root().set_default_widget(None) if shift_button.get_root() else None)
                obj.add_controller(focus_controller)
                
            for axis in "XYZ":
                for name_template in ("AlignPosition%s", "AlignPosition%sMin",
                                      "AlignPosition%sCenter", "AlignPosition%sMax"):
                    obj = self.gui.get_object(name_template % axis)
                    focus_controller = self._gtk.EventControllerFocus.new()
                    focus_controller.connect("enter", lambda controller: align_button.grab_default())
                    focus_controller.connect("leave", lambda controller: 
                        align_button.get_root().set_default_widget(None) if align_button.get_root() else None)
                    obj.add_controller(focus_controller)
            self._event_handlers = (("model-selection-changed", self._update_position_widgets), )
            self.register_gtk_handlers(self._gtk_handlers)
            self.register_event_handlers(self._event_handlers)
            self._update_position_widgets()
        return True

    def teardown(self):
        if self.gui:
            self.unregister_event_handlers(self._event_handlers)
            self.unregister_gtk_handlers(self._gtk_handlers)
            self.core.unregister_ui("model_handling", self.gui.get_object("ModelPositionBox"))

    def _update_position_widgets(self):
        widget = self.gui.get_object("ModelPositionBox")
        if self.core.get("models").get_selected():
            widget.show()
        else:
            widget.hide()

    def _shift_model(self, widget=None):
        models = self.core.get("models").get_selected()
        if not models:
            return
        axes = [self.gui.get_object("ShiftPosition%s" % axis).get_value() for axis in "XYZ"]
        shift_operation = {"action": "shift", "shift_target": "distance", "axes": axes}
        for model in models:
            model.extend_value("transformations", [shift_operation])

    def _align_model(self, widget=None):
        models = self.core.get("models").get_selected()
        if not models:
            return
        transformations = []
        # collect transformations for min/center/max alignments
        # Each alignment transformation is only added, if it was selected for at least one axis.
        for obj_name_suffix, shift_target in (("Min", "align_min"),
                                              ("Center", "center"),
                                              ("Max", "align_max")):
            axes = [None, None, None]
            for index, axis in enumerate("XYZ"):
                objname = "AlignPosition%s%s" % (axis, obj_name_suffix)
                if self.gui.get_object(objname).get_active():
                    axes[index] = self.gui.get_object("AlignPosition%s" % axis).get_value()
            if any(axis is not None for axis in axes):
                transformations.append(
                    {"action": "shift", "shift_target": shift_target, "axes": axes})
        for model in models:
            model.extend_value("transformations", transformations)
