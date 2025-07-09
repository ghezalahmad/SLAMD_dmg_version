#!/bin/bash

# Build script for SLAMD macOS app with improved error handling

echo "🚀 Building SLAMD macOS App..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Please install it with:"
    echo "   pip install pyinstaller"
    exit 1
fi

# Check if spec file exists
if [ ! -f "run_slamd.spec" ]; then
    echo "❌ run_slamd.spec not found in current directory"
    exit 1
fi

# Check if main Python file exists
if [ ! -f "run_slamd.py" ]; then
    echo "❌ run_slamd.py not found in current directory"
    exit 1
fi

# Check if slamd directory exists
if [ ! -d "slamd" ]; then
    echo "❌ slamd directory not found. Make sure you're in the right directory."
    exit 1
fi

# Check if JAR files exist
if [ ! -f "slamd/jars/lolo-0.7.3.jar" ]; then
    echo "❌ lolo-0.7.3.jar not found in slamd/jars/"
    exit 1
fi

if [ ! -f "slamd/jars/py4j-0.10.9.7.jar" ]; then
    echo "❌ py4j-0.10.9.7.jar not found in slamd/jars/"
    exit 1
fi

echo "✅ All required files found"

# Clean previous builds
if [ -d "dist" ]; then
    echo "🧹 Cleaning previous builds..."
    rm -rf dist
fi

if [ -d "build" ]; then
    rm -rf build
fi

# Remove any existing log files
if [ -f "slamd_debug.log" ]; then
    rm -f slamd_debug.log
fi

if [ -f "app_debug.log" ]; then
    rm -f app_debug.log
fi

# Build the app
echo "🔨 Running PyInstaller..."
pyinstaller --clean run_slamd.spec

# Check if build was successful
if [ -d "dist/SLAMD.app" ]; then
    echo "✅ Build successful!"
    echo "📦 App created at: dist/SLAMD.app"
    
    # Make the app executable
    chmod +x "dist/SLAMD.app/Contents/MacOS/SLAMD"
    
    # Set proper permissions for the entire app bundle
    chmod -R 755 "dist/SLAMD.app"
    
    # Create debug script
    cat > debug_app.sh << 'EOF'
#!/bin/bash
echo "🔍 Running SLAMD in debug mode..."
./dist/SLAMD.app/Contents/MacOS/SLAMD
EOF
    chmod +x debug_app.sh
    
    echo "🔍 Debug script created: debug_app.sh"
    
    # Test if the app can be launched
    echo "🧪 Testing app launch..."
    timeout 10s ./dist/SLAMD.app/Contents/MacOS/SLAMD &
    TEST_PID=$!
    sleep 5
    
    if kill -0 $TEST_PID 2>/dev/null; then
        echo "✅ App launches successfully!"
        kill $TEST_PID 2>/dev/null
        wait $TEST_PID 2>/dev/null
    else
        echo "⚠️  App may have issues. Check debug output above."
    fi
    
    echo ""
    echo "🎉 Build complete!"
    echo "   • Double-click dist/SLAMD.app to run"
    echo "   • Run ./debug_app.sh to see debug output"
    echo "   • Check slamd_debug.log for detailed logs"
    echo ""
    
    # Ask about DMG creation
    read -p "📦 Create DMG file for distribution? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Creating DMG..."
        
        # Create a temporary directory for DMG contents
        mkdir -p dist/dmg_temp
        cp -R dist/SLAMD.app dist/dmg_temp/
        
        # Create a simple DMG
        if command -v create-dmg &> /dev/null; then
            create-dmg \
                --volname "SLAMD Installer" \
                --window-pos 200 120 \
                --window-size 800 600 \
                --icon-size 100 \
                --icon "SLAMD.app" 200 190 \
                --hide-extension "SLAMD.app" \
                --app-drop-link 600 185 \
                "dist/SLAMD-Installer.dmg" \
                "dist/dmg_temp/"
            echo "✅ DMG created at: dist/SLAMD-Installer.dmg"
        else
            # Fallback to hdiutil
            hdiutil create -volname "SLAMD Installer" -srcfolder "dist/dmg_temp" -ov -format UDZO "dist/SLAMD-Installer.dmg"
            echo "✅ DMG created at: dist/SLAMD-Installer.dmg"
        fi
        
        # Clean up temporary directory
        rm -rf dist/dmg_temp
    fi
    
else
    echo "❌ Build failed. Check the output above for errors."
    echo "Common issues:"
    echo "  • Missing dependencies (install with pip)"
    echo "  • Path issues with slamd modules"
    echo "  • JAR files not found"
    echo ""
    echo "Try running with debug output:"
    echo "  pyinstaller --clean --debug all run_slamd.spec"
    exit 1
fi