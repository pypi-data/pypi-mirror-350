# Debug script to trace the connection issue
from easyremote import Client
import traceback

def debug_connection():
    """Debug the connection issue step by step."""
    print("🔍 Debugging EasyRemote Connection Issue")
    print("=" * 60)
    
    try:
        print("Step 1: Creating client...")
        client = Client("localhost:8080")
        print(f"   ✅ Client created: {type(client)}")
        print(f"   📍 Gateway address: {client.gateway_address}")
        print(f"   🆔 Client ID: {client.client_id}")
        
        print("\nStep 2: Checking connection state...")
        print(f"   📊 Connection state: {client._connection_state}")
        
        print("\nStep 3: Attempting manual connection...")
        try:
            client.connect()
            print("   ✅ Connection successful!")
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            print(f"   🔍 Exception type: {type(e)}")
            print(f"   📍 Gateway address at error: {client.gateway_address}")
            
            # Check if it's our custom exception
            if hasattr(e, 'error_context'):
                print(f"   📋 Error context: {e.error_context.additional_data}")
            
            # Print full traceback
            print("\n   📜 Full traceback:")
            traceback.print_exc()
            
            # Check if there's a cause chain
            current = e
            level = 1
            while hasattr(current, 'cause') and current.cause:
                current = current.cause
                print(f"\n   🔗 Cause level {level}: {type(current)} - {current}")
                level += 1
        
        print("\nStep 4: Testing execute (which triggers auto-connect)...")
        try:
            result = client.execute("test_function")
            print(f"   ✅ Execute successful: {result}")
        except Exception as e:
            print(f"   ❌ Execute failed: {e}")
            print(f"   🔍 Exception type: {type(e)}")
            print(f"   📍 Gateway address at error: {client.gateway_address}")
            
    except Exception as e:
        print(f"❌ Failed during setup: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_connection() 