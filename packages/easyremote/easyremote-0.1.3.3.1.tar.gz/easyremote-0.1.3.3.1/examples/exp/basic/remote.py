# Improved EasyRemote client with better error handling
from easyremote import Client
import sys

def main():
    """Main client function with improved error handling."""
    print("🚀 EasyRemote Client Demo")
    print("=" * 50)
    
    try:
        # Connect to the gateway server
        print("🔗 Connecting to gateway server...")
        client = Client("localhost:8080")
        print(f"✅ Client initialized with address: {client.gateway_address}")
        
        # Test basic functions
        print("\n📊 Testing remote function calls...")
        
        # Test 1: Simple addition
        print("\n1️⃣ Testing add_numbers function:")
        try:
            result1 = client.execute("add_numbers", 10, 20)
            print(f"   add_numbers(10, 20) = {result1}")
        except Exception as e:
            print(f"   ❌ add_numbers failed: {e}")
        
        # Test 2: AI inference
        print("\n2️⃣ Testing ai_inference function:")
        try:
            result2 = client.execute("ai_inference", "Hello World")
            print(f"   ai_inference('Hello World') = {result2}")
        except Exception as e:
            print(f"   ❌ ai_inference failed: {e}")
        
        # Test 3: Multiplication
        print("\n3️⃣ Testing multiply_numbers function:")
        try:
            result3 = client.execute("multiply_numbers", 5, 6)
            print(f"   multiply_numbers(5, 6) = {result3}")
        except Exception as e:
            print(f"   ❌ multiply_numbers failed: {e}")
        
        # Test 4: List processing
        print("\n4️⃣ Testing process_list function:")
        try:
            test_list = [1, 2, 3, 4, 5]
            result4 = client.execute("process_list", test_list)
            print(f"   process_list({test_list}) = {result4}")
        except Exception as e:
            print(f"   ❌ process_list failed: {e}")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Client failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide helpful troubleshooting information
        print("\n💡 Troubleshooting steps:")
        print("  1. Make sure the gateway server is running:")
        print("     python vps_server.py")
        print("  2. Make sure at least one compute node is running:")
        print("     python compute_node.py") 
        print("  3. Check if localhost:8080 is accessible")
        print("  4. Verify no firewall is blocking the connection")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
