#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify the gRPC keepalive fix for EasyRemote framework.

This script tests the basic functionality with enhanced logging to ensure
the "too_many_pings" error has been resolved.
"""

import time
import logging
from easyremote import Client

# Configure logging to see detailed execution
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

def test_remote_execution():
    """Test remote function execution with detailed logging."""
    
    print("🚀 Starting EasyRemote keepalive fix test...")
    print("="*60)
    
    # Connect to the gateway server
    print("📡 Connecting to gateway at localhost:8080...")
    client = Client("localhost:8080")
    
    try:
        # Test basic function call
        print("\n🔢 Testing basic arithmetic function...")
        result1 = client.execute("add_numbers", 15, 25)
        print(f"✅ add_numbers(15, 25) = {result1}")
        
        # Test AI inference function
        print("\n🤖 Testing AI inference function...")
        result2 = client.execute("ai_inference", "Hello from the fixed system!")
        print(f"✅ ai_inference result: {result2}")
        
        # Test multiple calls to stress test the connection
        print("\n🔄 Testing multiple consecutive calls...")
        for i in range(5):
            start_time = time.time()
            result = client.execute("add_numbers", i, i * 2)
            duration = (time.time() - start_time) * 1000
            print(f"📊 Call {i+1}: add_numbers({i}, {i*2}) = {result} (took {duration:.1f}ms)")
            time.sleep(1)  # Small delay between calls
        
        # Test connection stability with longer wait
        print("\n⏱️  Testing connection stability (waiting 35 seconds to test keepalive)...")
        print("    This tests if the keepalive fix prevents connection issues...")
        
        for countdown in range(35, 0, -5):
            print(f"    ⏳ Waiting {countdown} more seconds...")
            time.sleep(5)
        
        # Execute after long wait
        print("\n🎯 Executing function after long wait...")
        result3 = client.execute("add_numbers", 100, 200)
        print(f"✅ Post-wait result: add_numbers(100, 200) = {result3}")
        
        print("\n🎉 SUCCESS! All tests passed - keepalive fix is working!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        print("❌ Test failed - there may still be connection issues")
        print("="*60)
        return False

if __name__ == "__main__":
    success = test_remote_execution()
    exit(0 if success else 1) 