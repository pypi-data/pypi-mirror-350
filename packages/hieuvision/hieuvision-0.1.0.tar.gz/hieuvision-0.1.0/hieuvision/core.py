from hieuvision.tools.augmenter import ImageAugmenter

class HieuVision:
    def __init__(self):
        self.tools = {}

    def add_tool(self, name, tool_instance):
        self.tools[name] = tool_instance

    def run_tool(self, name):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found.")
        print(f"Running tool: {name}")
        self.tools[name].run()