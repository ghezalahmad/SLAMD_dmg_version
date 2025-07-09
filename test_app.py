#!/usr/bin/env python3
"""
Simple test script to verify all dependencies are working
Run this before building the app to catch issues early
"""

import sys
import os
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    modules_to_test = [
        'flask',
        'jinja2', 
        'py4j',
        'lolopy',
        'werkzeug',
        'pandas',
        'numpy',
        'scipy',
        'sklearn',
        'plotly',
        'flask_cors',
        'flask_wtf',
        'flask_session',
        'PIL.Image',
        'inspect',
        'threading',
        'webbrowser',
        'time',
        'subprocess'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} modules failed to import:")
        for module in failed_imports:
            print(f"  - {module}")
        print("\nInstall missing modules with:")
        print(f"  pip install {' '.join(failed_imports)}")
        return False
    else:
        print(f"\n✅ All {len(modules_to_test)} modules imported successfully!")
        return True

def test_files():
    """Test if all required files exist"""
    print("\n📁 Testing file existence...")
    
    required_files = [
        'run_slamd.py',
        'run_slamd.spec',
        'slamd/jars/lolo-0.7.3.jar',
        'slamd/jars/py4j-0.10.9.7.jar'
    ]
    
    required_dirs = [
        'slamd',
        'slamd/templates',
        'slamd/static',
        'slamd/common',
        'slamd/discovery',
        'slamd/formulations',
        'slamd/materials',
        'slamd/design_assistant',
        'slamd/jars'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        print(f"\n❌ Missing files/directories:")
        for item in missing_files + missing_dirs:
            print(f"  - {item}")
        return False
    else:
        print(f"\n✅ All required files and directories found!")
        return True

def test_slamd_import():
    """Test if slamd module can be imported"""
    print("\n🔍 Testing slamd module import...")
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        from slamd import create_app
        print("✅ slamd.create_app imported successfully")
        
        # Test app creation
        template_folder = os.path.join(os.getcwd(), 'slamd', 'templates')
        static_folder = os.path.join(os.getcwd(), 'slamd', 'static')
        
        app = create_app(template_folder=template_folder, static_folder=static_folder)
        print("✅ Flask app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error importing slamd: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_jar_files():
    """Test if JAR files can be read"""
    print("\n📦 Testing JAR file accessibility...")
    
    jar_files = [
        'slamd/jars/lolo-0.7.3.jar',
        'slamd/jars/py4j-0.10.9.7.jar'
    ]
    
    for jar_path in jar_files:
        try:
            with open(jar_path, 'rb') as f:
                # Read first few bytes to verify file is readable
                data = f.read(100)
                if data:
                    print(f"✅ {jar_path} is readable ({len(data)} bytes read)")
                else:
                    print(f"❌ {jar_path} is empty")
                    return False
        except Exception as e:
            print(f"❌ Error reading {jar_path}: {e}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 SLAMD App Pre-Build Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("File Existence", test_files),
        ("JAR Files", test_jar_files),
        ("SLAMD Module", test_slamd_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready to build the app.")
        print("Run: ./build_app.sh")
        return True
    else:
        print("❌ Some tests failed. Fix the issues before building.")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)