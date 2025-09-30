#!/usr/bin/env python3
"""
Test runner for Pipeline Monitor
Runs all tests without pytest dependency issues
"""

import sys
import importlib
from datetime import datetime

def run_test_module(module_name):
    """Run all tests in a module"""
    print(f"\n🔧 Running {module_name}...")
    try:
        module = importlib.import_module(module_name)
        
        # Find and run test functions
        test_functions = [func for func in dir(module) if func.startswith('test_')]
        
        for test_func in test_functions:
            print(f"  🧪 {test_func}...", end=" ")
            try:
                getattr(module, test_func)()
                print("✅ PASSED")
            except Exception as e:
                print(f"❌ FAILED: {e}")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False

def main():
    print("🚀 Pipeline Monitor Test Suite")
    print("=" * 50)
    
    test_modules = [
        "tests.test_basic",
        "tests.test_monitor", 
        "tests.test_alerts",
        "tests.test_recovery"
    ]
    
    passed = 0
    failed = 0
    
    for module in test_modules:
        if run_test_module(module):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📅 Completed at: {datetime.now()}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()