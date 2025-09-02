#!/usr/bin/env python3

import os
import sys

# Add the pycam path for imports
sys.path.insert(0, '/Users/charolastra/hack/pycam')

import pycam.Utils
from gi.repository import Gtk

def test_file_filter():
    """Test file filter creation and pattern matching"""
    
    print("Testing file filter patterns...")
    
    # Test the case insensitive pattern function
    patterns = ["*.stl", "*.dxf", "*.svg"]
    for pattern in patterns:
        case_insensitive = pycam.Utils.get_case_insensitive_file_pattern(pattern)
        print(f"  {pattern} -> {case_insensitive}")
    
    print("\nTesting GTK FileFilter creation...")
    
    # Create a filter similar to what FilenameDialog does
    file_filter = Gtk.FileFilter()
    file_filter.set_name("STL models")
    
    # Add patterns
    stl_pattern = pycam.Utils.get_case_insensitive_file_pattern("*.stl")
    print(f"Adding pattern: {stl_pattern}")
    file_filter.add_pattern(stl_pattern)
    
    # Also try adding mime type
    file_filter.add_mime_type("model/stl")
    
    print("FileFilter created successfully")
    
    # Test some filenames
    test_files = ["model.stl", "Model.STL", "test.dxf", "example.svg"]
    for filename in test_files:
        print(f"  Testing filename: {filename}")

if __name__ == "__main__":
    test_file_filter()