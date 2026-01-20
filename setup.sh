#!/bin/bash
# Setup script for Clouds Detangler

echo "Setting up Clouds Detangler..."
echo "==============================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Make the main script executable
chmod +x clouds_detangler.py
echo "✓ Made clouds_detangler.py executable"

# Copy example config if config doesn't exist
if [ ! -f config.json ]; then
    cp config.example.json config.json
    echo "✓ Created config.json from example"
else
    echo "• config.json already exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To run the tool:"
echo "  python3 clouds_detangler.py"
echo ""
echo "Or:"
echo "  ./clouds_detangler.py"
