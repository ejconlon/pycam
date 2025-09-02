#!/bin/bash

# Script to validate all .ui XML files using xmllint

echo "Validating .ui XML files..."
echo "=========================="

# Find all .ui files and validate them
exit_code=0

for file in /Users/charolastra/hack/pycam/share/ui/*.ui; do
    echo "Checking $file"
    if xmllint --noout "$file" 2>/dev/null; then
        echo "✓ Valid: $(basename "$file")"
    else
        echo "✗ Invalid: $(basename "$file")"
        echo "  Error details:"
        xmllint --noout "$file"
        exit_code=1
    fi
    echo ""
done

if [ $exit_code -eq 0 ]; then
    echo "All .ui files are valid XML!"
else
    echo "Some .ui files have XML validation errors."
fi

exit $exit_code