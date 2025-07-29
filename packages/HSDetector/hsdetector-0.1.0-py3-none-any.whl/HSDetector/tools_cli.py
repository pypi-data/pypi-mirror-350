# HSDetector/tools_cli.py

import sys
import importlib

def main():
    if len(sys.argv) < 2:
        print("Usage: HSDetector_tools <tool_name> [args...]")
        sys.exit(1)

    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]

    try:
        module = importlib.import_module(f"HSDetector.tools.{tool_name}")
    except ImportError:
        print(f"Tool '{tool_name}' not found.")
        sys.exit(1)

    sys.argv = [f"{tool_name}.py"] + tool_args  # Properly reset sys.argv
    if hasattr(module, 'main'):
        module.main()
    else:
        print(f"Tool '{tool_name}' does not have a main() function.")
        sys.exit(1)
