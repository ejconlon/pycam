#!/usr/bin/env python3

import re

def fix_final_issues():
    # Fix GtkEventBox in log.ui
    with open('share/ui/log.ui', 'r') as f:
        content = f.read()
    
    # Replace GtkEventBox with GtkBox
    content = re.sub(r'<object class="GtkEventBox"', '<object class="GtkBox"', content)
    
    with open('share/ui/log.ui', 'w') as f:
        f.write(content)
    print("Fixed GtkEventBox in log.ui")
    
    # Fix image_position in model_position.ui
    with open('share/ui/model_position.ui', 'r') as f:
        content = f.read()
    
    # Remove image_position property
    content = re.sub(r'[ \t]*<property name="image_position">.*?</property>\n', '', content)
    
    with open('share/ui/model_position.ui', 'w') as f:
        f.write(content)
    print("Fixed image_position in model_position.ui")

if __name__ == '__main__':
    fix_final_issues()
    print("Done fixing final two issues")