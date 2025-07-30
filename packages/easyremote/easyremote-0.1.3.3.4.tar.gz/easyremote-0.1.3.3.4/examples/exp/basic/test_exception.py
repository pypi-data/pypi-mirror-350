# Test the ConnectionError constructor directly
from easyremote.core.utils.exceptions import ConnectionError
import traceback

def test_connection_error():
    """Test the ConnectionError constructor."""
    print("Testing ConnectionError constructor...")
    print("=" * 50)
    
    # Test 1: Normal case with address
    print("\n🔍 Test 1: Normal case with address")
    try:
        error1 = ConnectionError(
            message="Connection failed to localhost:8080",
            address="localhost:8080"
        )
        print(f"✅ Test 1 passed: {error1}")
        print(f"   Message: {error1.message}")
        print(f"   Context: {error1.error_context.additional_data}")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        traceback.print_exc()
    
    # Test 2: Case with None address
    print("\n🔍 Test 2: Case with None address")
    try:
        error2 = ConnectionError(
            message="Connection failed to localhost:8080", 
            address=None
        )
        print(f"✅ Test 2 passed: {error2}")
        print(f"   Message: {error2.message}")
        print(f"   Context: {error2.error_context.additional_data}")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        traceback.print_exc()
    
    # Test 3: Case with empty message and valid address
    print("\n🔍 Test 3: Case with empty message and valid address")
    try:
        error3 = ConnectionError(
            message="",
            address="localhost:8080"
        )
        print(f"✅ Test 3 passed: {error3}")
        print(f"   Message: {error3.message}")
        print(f"   Context: {error3.error_context.additional_data}")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        traceback.print_exc()
    
    # Test 4: Case with empty message and None address
    print("\n🔍 Test 4: Case with empty message and None address")
    try:
        error4 = ConnectionError(
            message="",
            address=None
        )
        print(f"✅ Test 4 passed: {error4}")
        print(f"   Message: {error4.message}")
        print(f"   Context: {error4.error_context.additional_data}")
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_connection_error() 