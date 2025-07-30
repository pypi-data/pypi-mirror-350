# Example compute node for EasyRemote
from easyremote import ComputeNode
import time

def main():
    """Start the compute node."""
    print("🚀 Starting EasyRemote Compute Node...")
    print("=" * 50)
    
    try:
        # Connect to the gateway server
        node = ComputeNode("localhost:8080")
        print(f"✅ Connected to gateway at localhost:8080")
        
        # Register functions
        print("📝 Registering functions...")
        
        @node.register
        def add_numbers(a, b):
            """Simple addition function."""
            print(f"Computing: {a} + {b}")
            return a + b
        
        @node.register
        def multiply_numbers(a, b):
            """Simple multiplication function."""
            print(f"Computing: {a} * {b}")
            return a * b
        
        @node.register
        def ai_inference(text):
            """Mock AI inference function."""
            print(f"Processing text: {text}")
            # Simulate some processing time
            time.sleep(0.1)
            return f"AI processing result: {text.upper()}"
        
        @node.register
        def process_list(data_list):
            """Process a list of numbers."""
            print(f"Processing list of {len(data_list)} items")
            return [x * 2 for x in data_list]
        
        print("✅ Functions registered:")
        print("  - add_numbers(a, b)")
        print("  - multiply_numbers(a, b)")  
        print("  - ai_inference(text)")
        print("  - process_list(data_list)")
        
        print("\n🏃 Starting to serve requests...")
        print("Press Ctrl+C to stop the node")
        
        # Start serving (this will block)
        node.serve()
        
    except KeyboardInterrupt:
        print("\n🛑 Compute node stopped by user")
    except Exception as e:
        print(f"❌ Failed to start compute node: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Common troubleshooting tips
        print("\n💡 Troubleshooting:")
        print("  1. Make sure the gateway server is running at localhost:8080")
        print("  2. Check network connectivity")
        print("  3. Verify the gateway address is correct")

if __name__ == "__main__":
    main() 