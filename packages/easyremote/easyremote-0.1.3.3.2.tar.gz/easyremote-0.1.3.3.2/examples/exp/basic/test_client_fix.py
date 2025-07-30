# Test script to diagnose and verify the client connection fix
from easyremote import Client
import sys

def test_client_initialization():
    """Test if the client can be initialized properly."""
    print("🔍 Testing Client initialization...")
    
    try:
        # Test with proper address
        client = Client("localhost:8080")
        print(f"✅ Client initialized successfully with address: {client.gateway_address}")
        return client
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return None

def test_client_connection():
    """Test client connection with improved error handling."""
    print("\n🔍 Testing Client connection...")
    
    client = test_client_initialization()
    if not client:
        return False
    
    try:
        # This will trigger the connection attempt
        print("Attempting to connect...")
        client.connect()
        print("✅ Client connected successfully!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_graceful_failure():
    """Test that client fails gracefully when server is not available."""
    print("\n🔍 Testing graceful failure handling...")
    
    client = test_client_initialization()
    if not client:
        return False
    
    try:
        # Try to execute a function (this should trigger auto-connection)
        result = client.execute("add_numbers", 10, 20)
        print("✅ Function executed successfully (server is running)")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"⚠️  Expected failure: {e}")
        print("This is expected if no server is running at localhost:8080")
        return False

if __name__ == "__main__":
    print("🚀 EasyRemote Client Connection Test")
    print("=" * 50)
    
    # Run tests
    init_success = test_client_initialization() is not None
    conn_success = test_client_connection()
    exec_success = test_graceful_failure()
    
    print("\n📊 Test Results:")
    print(f"  Initialization: {'✅ PASS' if init_success else '❌ FAIL'}")
    print(f"  Connection:     {'✅ PASS' if conn_success else '❌ FAIL'}")
    print(f"  Execution:      {'✅ PASS' if exec_success else '⚠️  EXPECTED FAIL'}")
    
    if init_success and not conn_success:
        print("\n💡 Tips:")
        print("  1. Make sure a gateway server is running at localhost:8080")
        print("  2. Check if the port is correct and accessible")
        print("  3. Verify your firewall settings")
    
    print("\n🎯 To start a complete EasyRemote setup:")
    print("  1. Start gateway server: python vps_server.py")
    print("  2. Start compute node: python compute_node.py")
    print("  3. Run client: python remote.py") 