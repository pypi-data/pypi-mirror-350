#!/bin/bash

set -e  # Exit on error

# Activate conda env
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate egi-jupyterlab-ext
echo "Conda environment 'jupyterlab-ext' activated."

# Auto-increment version in package.json
echo "Bumping package.json version..."
PACKAGE_JSON="package.json"

# Bump patch version using jq
if command -v jq &> /dev/null; then
    current_version=$(jq -r .version "$PACKAGE_JSON")
    IFS='.' read -r major minor patch <<< "$current_version"
    new_version="${major}.${minor}.$((patch + 1))"
    jq ".version = \"$new_version\"" "$PACKAGE_JSON" > tmp.json && mv tmp.json "$PACKAGE_JSON"
    echo "Updated version to $new_version in $PACKAGE_JSON"
else
    echo "ERROR: jq not found. Please install jq to auto-bump version."
    exit 1
fi

# Clean old builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "Building the package..."
python3 -m venv build-env
source build-env/bin/activate
pip install build
python3 -m build -s

# Upload to PyPI
echo "Uploading the package to PyPI..."
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*

echo "Package uploaded successfully."
echo "+-------------------------------------------------"
echo "DONE :)"
