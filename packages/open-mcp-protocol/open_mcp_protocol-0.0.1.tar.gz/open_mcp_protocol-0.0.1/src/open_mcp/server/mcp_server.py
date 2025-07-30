class MCPServer:
    """Sample MCPServer class."""
    def __init__(self):
        self.status = "initialized"

    def start(self):
        self.status = "running"
        print("MCPServer started.")

    def stop(self):
        self.status = "stopped"
        print("MCPServer stopped.")
