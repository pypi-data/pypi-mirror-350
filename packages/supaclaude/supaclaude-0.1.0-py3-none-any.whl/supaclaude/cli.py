#!/usr/bin/env python3

import subprocess
import sys
import json
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich import box


def main():
    args = sys.argv[1:]
    console = Console()
    
    # Check if --output-format stream-json is in the arguments
    stream_json_mode = False
    for i, arg in enumerate(args):
        if arg == "--output-format" and i + 1 < len(args) and args[i + 1] == "stream-json":
            stream_json_mode = True
            break
    
    # Run the claude command with all arguments
    process = subprocess.Popen(
        ["claude"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    if stream_json_mode:
        # Parse and pretty print JSON stream
        for line in process.stdout:
            line = line.strip()
            if line:
                try:
                    json_obj = json.loads(line)
                    json_panel = Panel(JSON.from_data(json_obj), border_style="cyan", box=box.ROUNDED)
                    console.print(json_panel)
                except json.JSONDecodeError:
                    # If it's not valid JSON, print as-is
                    console.print(Panel(line, border_style="yellow", box=box.ROUNDED))
    else:
        # Pass through output as-is
        for line in process.stdout:
            print(line, end='')
    
    # Also print any stderr output
    stderr_output = process.stderr.read()
    if stderr_output:
        print(stderr_output, file=sys.stderr)
    
    # Wait for process to complete and exit with same code
    return_code = process.wait()
    sys.exit(return_code)


if __name__ == "__main__":
    main()