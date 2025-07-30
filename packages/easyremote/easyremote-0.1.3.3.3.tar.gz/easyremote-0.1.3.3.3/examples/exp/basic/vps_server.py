# Example gateway server for EasyRemote
from easyremote import Server

def main():
    """Start the gateway server."""
    print("🚀 Starting EasyRemote Gateway Server...")
    print("=" * 50)
    
    try:
        # Create and start the gateway server
        server = Server(port=8080)
        print(f"✅ Gateway server initialized on port 8080")
        print("📡 Server is ready to accept connections...")
        print("🔗 Compute nodes can connect to this server")
        print("🖥️  Clients can connect to localhost:8080")
        print("\nPress Ctrl+C to stop the server")
        
        # Start the server (this will block)
        server.start()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Common troubleshooting tips
        print("\n💡 Troubleshooting:")
        print("  1. Check if port 8080 is already in use")
        print("  2. Try running with administrator/sudo privileges")
        print("  3. Check firewall settings")

if __name__ == "__main__":
    main() 