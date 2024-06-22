#!/bin/sh

# References
# https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
# https://medium.com/@jackhuang.wz/in-just-two-steps-you-can-turn-a-python-script-into-a-macos-application-installer-6e21bce2ee71

# ---------------------------------------
# Clean up previous builds
# ---------------------------------------

echo "Cleaning up previous builds..."
rm -rf build dist/*

# ---------------------------------------
# Step 1: Convert Python script to an application bundle
# ---------------------------------------
echo "Converting Python script to macOS app bundle..."
# The following command will create a standalone .app from your Python script
pyinstaller --name 'Sbobbino' \
            --icon 'icon.png' \
            --windowed \
            --add-data='./requirements.txt:.' \
            sbobbino.py

# ---------------------------------------
# Step 2: Convert the application bundle to a DMG (macOS disk image)
# ---------------------------------------
echo "Creating DMG installer..."

# Prepare the folder for DMG creation
mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/Sbobbino.app" dist/dmg

# Create the DMG
# Ensure you have 'create-dmg' installed. If not, install using 'brew install create-dmg'
create-dmg \
  --volname "Sbobbino" \
  --volicon "icon.png" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Sbobbino.app" 175 120 \
  --hide-extension "Sbobbino.app" \
  --app-drop-link 425 120 \
  "dist/Sbobbino.dmg" \
  "dist/dmg/"

echo "Packaging complete. You can find the DMG installer in the dist/ directory."