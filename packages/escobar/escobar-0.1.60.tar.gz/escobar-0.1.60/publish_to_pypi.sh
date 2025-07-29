#!/bin/bash
# publish_to_pypi.sh - Script to publish to PyPI with automatic version increment

set -e  # Exit on any error

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found. Please create it with PYPI_TOKEN=your_token"
    exit 1
fi

# Check if PYPI_TOKEN is set
if [ -z "$PYPI_TOKEN" ]; then
    echo "Error: PYPI_TOKEN not found in .env file"
    exit 1
fi

# Get package name from pyproject.toml
PACKAGE_NAME=$(grep -m 1 'name = ' pyproject.toml | sed 's/name = "\(.*\)"/\1/')
echo "Package name: $PACKAGE_NAME"

# Get current version from package.json
ORIGINAL_VERSION=$(grep -m 1 '"version":' package.json | sed 's/.*"version": "\(.*\)",/\1/')
echo "Current version in package.json: $ORIGINAL_VERSION"

# Create a backup of package.json
cp package.json package.json.bak

# Make the Python script executable
chmod +x get_pypi_version.py

# Get the latest version from PyPI and calculate the new version
echo "Fetching latest version from PyPI..."
if python3 ./get_pypi_version.py "$PACKAGE_NAME" > version_info.txt; then
    # Successfully got version from PyPI
    source version_info.txt
    echo "Latest version on PyPI: $PYPI_VERSION"
    echo "New version to publish: $NEW_VERSION"
else
    # Failed to get version from PyPI, use local version + 1
    echo "Could not get version from PyPI. Using local version + 1."
    # Parse the version components
    MAJOR=$(echo $ORIGINAL_VERSION | cut -d. -f1)
    MINOR=$(echo $ORIGINAL_VERSION | cut -d. -f2)
    PATCH=$(echo $ORIGINAL_VERSION | cut -d. -f3)
    
    # If patch contains non-numeric characters, extract just the number part
    PATCH_NUM=$(echo $PATCH | grep -o '^[0-9]*')
    if [ -z "$PATCH_NUM" ]; then
        PATCH_NUM=0
    fi
    
    # Increment the patch version
    NEW_PATCH=$((PATCH_NUM + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
fi

echo "Will publish as version: $NEW_VERSION"

# Update the version in package.json
sed -i.tmp "s/\"version\": \"$ORIGINAL_VERSION\"/\"version\": \"$NEW_VERSION\"/" package.json
rm package.json.tmp

# Verify the version was updated correctly
UPDATED_VERSION=$(grep -m 1 '"version":' package.json | sed 's/.*"version": "\(.*\)",/\1/')
echo "Updated version in package.json: $UPDATED_VERSION"
if [ "$UPDATED_VERSION" != "$NEW_VERSION" ]; then
    echo "ERROR: Failed to update version in package.json. Aborting."
    mv package.json.bak package.json
    exit 1
fi

# Clean up temporary files
rm -f version_info.txt

# Do NOT restore the original version after publishing - keep the new version
RESTORE_VERSION=false

echo "Permanently updating version in package.json to $NEW_VERSION"

# Clean previous builds and dist directory
echo "Cleaning previous builds and dist directory..."
npm run clean:all
rm -rf dist/

# Install dependencies if needed
echo "Installing dependencies..."
npm install

# Build the extension
echo "Building the extension..."
npm run build:prod

# Build the Python package
echo "Building the Python package..."
python -m pip install --upgrade build
python -m build

# Check the built package
echo "Checking the built package..."
python -m pip install --upgrade twine
python -m twine check dist/*

# Upload to PyPI (only the current version)
echo "Uploading to PyPI (version $NEW_VERSION only)..."
python -m twine upload dist/*$NEW_VERSION* -u __token__ -p "$PYPI_TOKEN"

# Restore the original version in package.json if needed
if [ "$RESTORE_VERSION" = true ]; then
    echo "Restoring original version in package.json..."
    mv package.json.bak package.json
else
    echo "Keeping new version $NEW_VERSION in package.json"
    rm -f package.json.bak
fi

echo "Process completed!"
echo "If successful, your package should now be available at: https://pypi.org/project/$PACKAGE_NAME/"
echo "Users can install it with: pip install $PACKAGE_NAME"
echo "Published version: $NEW_VERSION"
