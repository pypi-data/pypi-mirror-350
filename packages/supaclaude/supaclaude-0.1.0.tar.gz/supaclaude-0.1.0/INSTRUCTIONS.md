

I want a python cli tool that wraps about the bash command tool "claude".

1. it passes whatever arguments directly to the claude command and print back whatever comes back from the claude command
2. if there is an argument `--output-format stream-json`, the cli will use rich print and print the json stream to the console


packages:
- rich