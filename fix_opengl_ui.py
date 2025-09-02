#!/usr/bin/env python3
"""Fix opengl.ui file structure issues"""

def fix_opengl_ui():
    filepath = "/Users/charolastra/hack/pycam/share/ui/opengl.ui"
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove all draw_indicator properties
    import re
    content = re.sub(r'\s*<property name="draw_indicator">True</property>\s*\n', '', content)
    
    # Fix the nested checkbox structure
    # Find the problematic section and replace it with proper GTK 4 structure
    old_section = '''    <child>
      <object class="GtkBox">
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkCheckButton" id="OpenGLLight">
            <property name="label" translatable="yes">Lighting</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <child>
              <object class="GtkCheckButton" id="OpenGLShadow">
                <property name="label" translatable="yes">Shadows</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">False</property>
                <property name="xalign">0.5</property>
            <child>
              <object class="GtkCheckButton" id="OpenGLPerspective">
                <property name="label" translatable="yes">Perspective view</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">False</property>
                <property name="xalign">0.5</property>
            <child>
              <object class="GtkCheckButton" id="OpenGLCache">'''
    
    new_section = '''    <child>
      <object class="GtkBox">
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkCheckButton" id="OpenGLLight">
            <property name="label" translatable="yes">Lighting</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
          </object>
        </child>
        <child>
          <object class="GtkCheckButton" id="OpenGLShadow">
            <property name="label" translatable="yes">Shadows</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
          </object>
        </child>
        <child>
          <object class="GtkCheckButton" id="OpenGLPerspective">
            <property name="label" translatable="yes">Perspective view</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
          </object>
        </child>
        <child>
          <object class="GtkCheckButton" id="OpenGLCache">'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("Fixed checkbox nesting structure")
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print("Fixed opengl.ui")

if __name__ == "__main__":
    fix_opengl_ui()